import { createAction, props } from '@ngrx/store';
import { UserProfileImage } from '../../models/user-profile-image';
import { UploadResponse } from '../../models/uploadfile_response';

export const loadProfileImage = createAction(
  '[Profile Image] Load',
  props<{ userId: number }>()
);

export const loadProfileImageSuccess = createAction(
  '[Profile Image] Load Success',
  props<{ record: UserProfileImage }>()
);

export const loadProfileImageNotFound = createAction(
  '[Profile Image] Not Found'
);

export const loadProfileImageFailure = createAction(
  '[Profile Image] Load Failure',
  props<{ error: string }>()
);

export const uploadProfileImage = createAction(
  '[Profile Image] Upload',
  props<{ file: File; userId: number }>()
);

// Updated to use the upload response directly
export const uploadProfileImageSuccess = createAction(
  '[Profile Image] Upload Success',
  props<{ 
    uploadResponse: UploadResponse;
    userId: number;
    existingFileId?: string | null;
  }>()
);

export const uploadProfileImageFailure = createAction(
  '[Profile Image] Upload Failure',
  props<{ error: string }>()
);

export const clearProfileImage = createAction('[Profile Image] Clear');

export { UploadResponse };
