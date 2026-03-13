import { createFeatureSelector, createSelector } from '@ngrx/store';
import { ProfileImageState } from './profile-image.reducer';

export const selectProfileImageState =
  createFeatureSelector<ProfileImageState>('profileImage');

export const selectProfileImageUrl = createSelector(
  selectProfileImageState,
  (s) => s.imageUrl
);

export const selectProfileImageUploading = createSelector(
  selectProfileImageState,
  (s) => s.uploading
);

export const selectProfileImageError = createSelector(
  selectProfileImageState,
  (s) => s.error
);

export const selectProfileFileId = createSelector(
  selectProfileImageState,
  (s) => s.record?.FileId ?? null
);