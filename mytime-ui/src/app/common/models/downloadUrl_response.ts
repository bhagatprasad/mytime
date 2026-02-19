export interface DownloadUrlResponse {
  success: boolean;
  url: string;
  expiresIn: number;
  expiresAt: number;
  fileId: string;
}