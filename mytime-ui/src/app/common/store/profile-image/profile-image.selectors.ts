import { createFeatureSelector, createSelector } from '@ngrx/store';
import { ProfileImageState } from './profile-image.reducer';

export const selectProfileImageState =
  createFeatureSelector<ProfileImageState>('profileImage');

export const selectProfileImageRecord = createSelector(
  selectProfileImageState,
  (s) => s.record
);

export const selectProfileImageUrl = createSelector(
  selectProfileImageState,
  (s) => s.imageUrl
);

export const selectProfileFileId = createSelector(
  selectProfileImageState,
  (s) => s.record?.FileId ?? null
);

export const selectProfileImageDbId = createSelector(
  selectProfileImageState,
  (s) => s.record?.Id ?? null
);

export const parseFileInfo = (fileInfoStr?: string): any => {
  if (!fileInfoStr) return null;
  try {
    return JSON.parse(fileInfoStr);
  } catch {
    return null;
  }
};

export const selectProfileFileInfo = createSelector(
  selectProfileImageRecord,
  (record) => parseFileInfo(record?.FileInfo)
);

export const selectProfileImageLoading = createSelector(
  selectProfileImageState,
  (s) => s.loading
);

export const selectProfileImageUploading = createSelector(
  selectProfileImageState,
  (s) => s.uploading
);

export const selectProfileImageError = createSelector(
  selectProfileImageState,
  (s) => s.error
);