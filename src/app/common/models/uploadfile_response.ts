export interface UploadResponse {
  success: boolean;
  fileId: string;
  fileName: string;
  storedFileName: string;
  contentType: string;
  contentLength: number;
  uploadTimestamp: number;
  downloadUrl: string;
}

