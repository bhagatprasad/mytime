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
import { Observable, Subject } from 'rxjs';
import { takeUntil, tap } from 'rxjs/operators';

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
        [class.is-uploading]="uploading$ | async"
        (click)="onContainerClick()"
        [title]="clickable ? 'Click to change profile photo' : ''"
      >
        <!-- Profile image -->
        <img
          [src]="imageUrl$ | async"
          [alt]="altText"
          class="profile-image"
          [ngClass]="size"
          (error)="onImageError($event)"
        />

        <!-- Spinner shown while uploading -->
        <div class="upload-overlay" *ngIf="uploading$ | async">
          <div class="spinner"></div>
        </div>

        <!-- Camera icon shown on hover when idle and clickable -->
        <div class="camera-overlay" *ngIf="clickable && !(uploading$ | async)">
          <i class="mdi mdi-camera"></i>
          <span>Change</span>
        </div>

        <!-- Hidden file input -->
        <input
          #fileInput
          type="file"
          accept="image/jpeg,image/png,image/webp,image/gif"
          style="display:none"
          (change)="onFileSelected($event)"
        />
      </div>

      <!-- Upload error message -->
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

  readonly imageUrl$: Observable<string> = this.store.select(
    selectProfileImageUrl
  );
  readonly uploading$: Observable<boolean> = this.store.select(
    selectProfileImageUploading
  );
  readonly error$: Observable<string | null> = this.store.select(
    selectProfileImageError
  );

  private currentUserId: number | null = null;
  private readonly destroy$ = new Subject<void>();

  constructor(
    private readonly store: Store,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit(): void {
    this.store
      .select(selectCurrentUser)
      .pipe(takeUntil(this.destroy$))
      .subscribe((user) => {
        this.currentUserId = user ? Number(user.id) : null;
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

    // Validate file type
    const validTypes = ['image/jpeg', 'image/png', 'image/webp', 'image/gif'];
    if (!validTypes.includes(file.type)) {
      alert('Please select a valid image file (JPEG, PNG, WEBP, or GIF)');
      return;
    }

    // Validate file size (5MB max)
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

  onImageError(event: Event): void {
    (event.target as HTMLImageElement).src = 'assets/images/faces/face28.png';
  }

  private get uploading(): boolean {
    let uploading = false;
    this.uploading$.pipe(takeUntil(this.destroy$)).subscribe((u) => (uploading = u));
    return uploading;
  }
}