import {
  Component,
  Input,
  OnInit,
  OnDestroy,
  ViewChild,
  ElementRef,
  ChangeDetectionStrategy,
  ChangeDetectorRef,
} from '@angular/core';
import { CommonModule } from '@angular/common';
import { Store } from '@ngrx/store';
import { Observable, Subject, combineLatest } from 'rxjs';
import { takeUntil, distinctUntilChanged, map } from 'rxjs/operators';
import {
  selectProfileImageUrl,
  selectProfileImageUploading,
  selectProfileImageError,
} from '../common/store/profile-image/profile-image.selectors';
import { selectCurrentUser } from '../common/store/auth.selectors';
import * as ProfileImageActions from '../common/store/profile-image/profile-image.actions';

@Component({
  selector: 'app-profile-image',
  standalone: true,
  imports: [CommonModule],
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    <div class="profile-image-wrapper">
      <div
        class="profile-image-container"
        [class.clickable]="clickable"
        [class.uploading]="uploading$ | async"
        (click)="onContainerClick()"
        [attr.title]="clickable ? 'Click to change profile photo' : null"
      >
        <img
          [src]="(imageUrl$ | async) || defaultImage"
          [alt]="altText"
          class="profile-image"
          [ngClass]="size"
          (error)="onImageError()"
        />

        <div class="upload-overlay" *ngIf="uploading$ | async">
          <div class="spinner"></div>
        </div>

        <div class="camera-overlay" *ngIf="showCamera$ | async">
          <span class="camera-icon">📷</span>
          <span class="camera-text">Change</span>
        </div>

        <input
          #fileInput
          type="file"
          accept="image/jpeg,image/png,image/webp,image/gif"
          (change)="onFileSelected($event)"
        />
      </div>

      <div *ngIf="error$ | async as err" class="upload-error">
        {{ err }}
      </div>
    </div>
  `,
  styles: [/* ... same styles ... */]
})
export class ProfileImageComponent implements OnInit, OnDestroy {
  @Input() size: 'small' | 'medium' | 'large' = 'large';
  @Input() clickable = true;
  @Input() altText = 'Profile Image';

  @ViewChild('fileInput') fileInput!: ElementRef<HTMLInputElement>;

  defaultImage = 'assets/images/faces/face28.png';
  
  readonly imageUrl$: Observable<string> = this.store.select(
    selectProfileImageUrl
  );
  readonly uploading$: Observable<boolean> = this.store.select(
    selectProfileImageUploading
  );
  readonly error$: Observable<string | null> = this.store.select(
    selectProfileImageError
  );

  readonly showCamera$: Observable<boolean>;

  private currentUserId: number | null = null;
  private readonly destroy$ = new Subject<void>();

  constructor(
    private readonly store: Store,
    private cdr: ChangeDetectorRef
  ) {
    this.showCamera$ = combineLatest([
      this.uploading$,
      this.store.select(selectCurrentUser).pipe(map(user => !!user))
    ]).pipe(
      map(([uploading, isLoggedIn]) => 
        this.clickable && !uploading && isLoggedIn
      )
    );
  }

  ngOnInit(): void {
    this.store
      .select(selectCurrentUser)
      .pipe(
        takeUntil(this.destroy$),
        distinctUntilChanged((prev, curr) => prev?.id === curr?.id)
      )
      .subscribe((user) => {
        const userId = user ? Number(user.id) : null;
        if (userId && this.currentUserId !== userId) {
          setTimeout(() => {
            this.store.dispatch(
              ProfileImageActions.loadProfileImage({ userId })
            );
          }, 100);
        }
        this.currentUserId = userId;
        this.cdr.markForCheck();
      });
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  onContainerClick(): void {
    if (this.clickable && !this.uploading) {
      this.fileInput.nativeElement.click();
    }
  }

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    const file = input.files?.[0];

    if (!file) return;
    
    if (!this.currentUserId) {
      alert('You must be logged in to upload a profile image');
      return;
    }

    const validTypes = ['image/jpeg', 'image/png', 'image/webp', 'image/gif'];
    if (!validTypes.includes(file.type)) {
      alert('Please select a valid image file (JPEG, PNG, WEBP, or GIF)');
      return;
    }

    if (file.size > 5 * 1024 * 1024) {
      alert('Image must be smaller than 5MB');
      return;
    }

    this.store.dispatch(
      ProfileImageActions.uploadProfileImage({
        file,
        userId: this.currentUserId,
      })
    );

    input.value = '';
  }

  onImageError(): void {
    console.log('Image failed to load, using default');
  }

  private get uploading(): boolean {
    let uploading = false;
    this.uploading$.pipe(takeUntil(this.destroy$)).subscribe((u) => (uploading = u));
    return uploading;
  }
}