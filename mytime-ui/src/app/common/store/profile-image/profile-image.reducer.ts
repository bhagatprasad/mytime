import { createReducer, on } from '@ngrx/store';
import * as A from './profile-image.actions';

export interface ProfileImageState {
  record: any | null;
  imageUrl: string;
  loading: boolean;
  uploading: boolean;
  error: string | null;
}

export const DEFAULT_PROFILE_IMAGE = 'assets/images/faces/face28.png';

export const initialProfileImageState: ProfileImageState = {
  record: null,
  imageUrl: DEFAULT_PROFILE_IMAGE,
  loading: false,
  uploading: false,
  error: null,
};

export function resolveImageUrl(record: any): string {
  if (!record?.FileInfo) return DEFAULT_PROFILE_IMAGE;
  
  try {
    const fileInfo = JSON.parse(record.FileInfo);
    return fileInfo.downloadUrl || DEFAULT_PROFILE_IMAGE;
  } catch {
    return DEFAULT_PROFILE_IMAGE;
  }
}

export const profileImageReducer = createReducer(
  initialProfileImageState,

  on(A.loadProfileImage, (state) => ({
    ...state,
    loading: true,
    error: null,
  })),

  on(A.loadProfileImageSuccess, (state, { record }) => ({
    ...state,
    record,
    imageUrl: resolveImageUrl(record),
    loading: false,
    error: null,
  })),

  on(A.loadProfileImageNotFound, (state) => ({
    ...state,
    record: null,
    imageUrl: DEFAULT_PROFILE_IMAGE,
    loading: false,
    error: null,
  })),

  on(A.loadProfileImageFailure, (state, { error }) => ({
    ...state,
    record: null,
    imageUrl: DEFAULT_PROFILE_IMAGE,
    loading: false,
    error,
  })),

  on(A.uploadProfileImage, (state) => ({
    ...state,
    uploading: true,
    error: null,
  })),

  // Don't update imageUrl here - wait for database save
  on(A.uploadProfileImageSuccess, (state) => ({
    ...state,
    uploading: true, // Keep uploading true until database save completes
    error: null,
  })),

  on(A.uploadProfileImageFailure, (state, { error }) => ({
    ...state,
    uploading: false,
    error,
  })),

  on(A.clearProfileImage, () => initialProfileImageState),
);