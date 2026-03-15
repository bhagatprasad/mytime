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
import { UserProfileImage } from '../../models/user-profile-image';
import { environment } from '../../../../environment';
import { AuditFieldsService } from '../../services/auditfields.service';
import { UploadResponse } from '../../models/uploadfile_response';

export const DEFAULT_PROFILE_IMAGE = 'assets/images/faces/face28.png';

@Injectable()
export class ProfileImageEffects {
  private readonly actions$ = inject(Actions);
  private readonly store = inject(Store);
  private readonly dbService = inject(UserProfileImageService);
  private readonly storageService = inject(StorageService);
  private readonly auditService = inject(AuditFieldsService);

  loadOnLogin$ = createEffect(() =>
    this.actions$.pipe(
      ofType(AuthActions.loginSuccess),
      map(({ user }) =>
        ProfileImageActions.loadProfileImage({ userId: Number(user.id) })
      )
    )
  );

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

  afterLoadSuccess$ = createEffect(() =>
    this.actions$.pipe(
      ofType(ProfileImageActions.loadProfileImageSuccess),
      switchMap(({ record }) => {
        const fileId = record?.FileId;
        const fileName = record?.FileName;
        
        if (fileId) {
          // Get a fresh signed URL from Backblaze using your working endpoint
          return from(this.storageService.getDownloadUrl(fileId)).pipe(
            map((response) => {
              console.log('Got signed URL:', response.url);
              return ProfileImageActions.loadProfileImageUrlSuccess({ 
                imageUrl: response.url 
              });
            }),
            catchError((err) => {
              console.error('Failed to get download URL:', err);
              return of(ProfileImageActions.loadProfileImageUrlFailure({ 
                error: 'Failed to load profile image' 
              }));
            })
          );
        }
        
        return of(ProfileImageActions.loadProfileImageUrlSuccess({ 
          imageUrl: DEFAULT_PROFILE_IMAGE 
        }));
      })
    )
  );

  upload$ = createEffect(() =>
    this.actions$.pipe(
      ofType(ProfileImageActions.uploadProfileImage),
      withLatestFrom(this.store.select(selectProfileFileId)),
      switchMap(([{ file, userId }, existingFileId]) => {
        return from(this.storageService.uploadFile(file, `profile_${userId}`)).pipe(
          map((uploadResponse: UploadResponse) => {
            return ProfileImageActions.uploadProfileImageSuccess({
              uploadResponse,
              userId,
              existingFileId
            });
          }),
          catchError((err) => {
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

  uploadSuccess$ = createEffect(() =>
    this.actions$.pipe(
      ofType(ProfileImageActions.uploadProfileImageSuccess),
      switchMap(({ uploadResponse, userId, existingFileId }) => {
        const payload: Partial<UserProfileImage> = {
          UserId: userId,
          FileId: uploadResponse.fileId,
          FileName: uploadResponse.fileName,
          BucketId: environment.UrlConstants?.Backblaze?.bucketId || '',
          ContentLength: uploadResponse.contentLength,
          ContentType: uploadResponse.contentType,
          FileInfo: JSON.stringify({
            downloadUrl: uploadResponse.downloadUrl,
            storedFileName: uploadResponse.storedFileName,
            uploadTimestamp: Date.now(),
          }),
        };

        return from(this.upsertInDatabase(payload)).pipe(
          map((savedRecord: UserProfileImage) => {
            if (existingFileId && existingFileId !== uploadResponse.fileId) {
              this.storageService.deleteFile(existingFileId).catch(() => {});
            }
            return ProfileImageActions.loadProfileImageSuccess({ record: savedRecord });
          }),
          catchError((err) => {
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