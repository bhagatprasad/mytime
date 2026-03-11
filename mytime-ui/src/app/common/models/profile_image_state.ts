import { ProfileFileInfo } from "./profile_fileInfo";
import { UserProfileImage } from "./user-profile-image";

export interface ProfileImageState {
  record:    UserProfileImage | null;
  imageUrl:  string; 
  loading:   boolean;
  uploading: boolean;
  error:     string | null;
}

export const DEFAULT_PROFILE_IMAGE = 'assets/images/faces/face28.png';

export const initialProfileImageState: ProfileImageState = {
  record:    null,
  imageUrl:  DEFAULT_PROFILE_IMAGE,
  loading:   false,
  uploading: false,
  error:     null,
};


export function parseFileInfo(fileInfo?: string | null): ProfileFileInfo | null {
  if (!fileInfo) return null;
  try {
    return JSON.parse(fileInfo) as ProfileFileInfo;
  } catch {
    return null;
  }
}

export function resolveImageUrl(record: UserProfileImage | null): string {
  if (!record) return DEFAULT_PROFILE_IMAGE;
  const info = parseFileInfo(record.FileInfo);
  return info?.downloadUrl || DEFAULT_PROFILE_IMAGE;
}
