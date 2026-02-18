export interface B2UploadResponse {
  fileId: string;
  fileName: string;
  bucketId: string;
  contentLength: number;
  contentType: string;
  contentSha1?: string;
  fileInfo: Record<string, string>;
  uploadTimestamp: number;
  action?: string;
}