import { Injectable, inject } from '@angular/core';
import { Actions, createEffect, ofType } from '@ngrx/effects';
import { Store } from '@ngrx/store';
import { of, from } from 'rxjs';
import { switchMap, map, catchError, withLatestFrom } from 'rxjs/operators';
import * as ProfileImageActions from './profile-image.actions';
import * as AuthActions from '../auth.actions';
import { selectProfileFileId } from './profile-image.selectors';

import { UserProfileImageService } from '../../services/user-profile-image.service';
import { StorageService } from '../../services/storage.service';
import { UploadResponse } from './profile-image.actions';
import { UserProfileImage } from '../../models/user-profile-image';
import { environment } from '../../../../environment';
import { AuditFieldsService } from '../../services/auditfields.service';

@Injectable()
export class ProfileImageEffects {
  private readonly actions$ = inject(Actions);
  private readonly store = inject(Store);
  private readonly dbService = inject(UserProfileImageService);
  private readonly storageService = inject(StorageService);
  private readonly auditService= inject(AuditFieldsService);
  // Load on login
  loadOnLogin$ = createEffect(() =>
    this.actions$.pipe(
      ofType(AuthActions.loginSuccess),
      map(({ user }) =>
        ProfileImageActions.loadProfileImage({ userId: Number(user.id) })
      )
    )
  );

  // Load profile image from database
  load$ = createEffect(() =>
    this.actions$.pipe(
      ofType(ProfileImageActions.loadProfileImage),
      switchMap(({ userId }) =>
        this.dbService.fetchProfileImageByUserAsync(userId).pipe(
          map((record) => {
            if (!record) {
              return ProfileImageActions.loadProfileImageNotFound();
            }
            return ProfileImageActions.loadProfileImageSuccess({ record });
          }),
          catchError((err) => {
            console.error('Error loading profile image:', err);
            if (err?.status === 404) {
              return of(ProfileImageActions.loadProfileImageNotFound());
            }
            return of(
              ProfileImageActions.loadProfileImageFailure({
                error: err?.message ?? 'Failed to load profile image',
              })
            );
          })
        )
      )
    )
  );

  // Upload profile image - simplified since upload API returns downloadUrl
  upload$ = createEffect(() =>
    this.actions$.pipe(
      ofType(ProfileImageActions.uploadProfileImage),
      withLatestFrom(this.store.select(selectProfileFileId)),
      switchMap(([{ file, userId }, existingFileId]) => {
        console.log('Uploading profile image for user:', userId);
        
        // Upload directly to storage service
        return from(this.storageService.uploadFile(file, `profile_${userId}`)).pipe(
          map((uploadResponse: UploadResponse) => {
            console.log('Upload successful, response:', uploadResponse);
            
            // Return success action with the upload response
            return ProfileImageActions.uploadProfileImageSuccess({
              uploadResponse,
              userId,
              existingFileId
            });
          }),
          catchError((err) => {
            console.error('Upload error:', err);
            return of(
              ProfileImageActions.uploadProfileImageFailure({
                error: err?.message ?? 'Upload failed. Please try again.',
              })
            );
          })
        );
      })
    )
  );

  // Handle upload success - save to database and delete old file
  uploadSuccess$ = createEffect(() =>
    this.actions$.pipe(
      ofType(ProfileImageActions.uploadProfileImageSuccess),
      switchMap(({ uploadResponse, userId, existingFileId }) => {
        console.log('Processing upload success, saving to database...');
        
        // Build FileInfo JSON using the downloadUrl from upload response
        const fileInfo = JSON.stringify({
          downloadUrl: uploadResponse.downloadUrl,
          storedFileName: uploadResponse.storedFileName,
          uploadTimestamp: uploadResponse.uploadTimestamp,
        });

        // Prepare database payload
        const payload: Partial<UserProfileImage> = {
          UserId: userId,
          FileId: uploadResponse.fileId,
          FileName: uploadResponse.fileName,
          BucketId: environment.UrlConstants?.Backblaze?.bucketId || '',
          ContentLength: uploadResponse.contentLength,
          ContentType: uploadResponse.contentType,
          FileInfo: fileInfo,
        };

        // Save to database
        return from(this.upsertInDatabase(payload)).pipe(
          map((savedRecord: UserProfileImage) => {
            console.log('Database record saved:', savedRecord);
            
            // Delete old file (fire and forget)
            if (existingFileId && existingFileId !== uploadResponse.fileId) {
              this.storageService.deleteFile(existingFileId).catch((err) => {
                console.warn('Could not delete old profile image:', err);
              });
            }
            
            // Return the saved record to update store
            return ProfileImageActions.loadProfileImageSuccess({ record: savedRecord });
          }),
          catchError((err) => {
            console.error('Database save error:', err);
            return of(
              ProfileImageActions.uploadProfileImageFailure({
                error: 'Image uploaded but failed to save to database',
              })
            );
          })
        );
      })
    )
  );

  // Clear on logout
  clearOnLogout$ = createEffect(() =>
    this.actions$.pipe(
      ofType(AuthActions.logout),
      map(() => ProfileImageActions.clearProfileImage())
    )
  );

  private upsertInDatabase(payload: Partial<UserProfileImage>): Promise<UserProfileImage> {
    
    return new Promise((resolve, reject) => {
      this.dbService.insertOrUpdateProfileImageAsync(this.auditService.appendAuditFields(payload)).subscribe({
        next: (record: UserProfileImage) => resolve(record),
        error: (err: any) => reject(err),
      });
    });
  }
}