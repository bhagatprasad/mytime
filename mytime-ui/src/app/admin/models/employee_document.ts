export interface EmployeeDocument {
  EmployeeDocumentId: number;
  EmployeeId?: number | null;
  DocumentType?: string | null;
  FileId?: string | null;
  FileName?: string | null;
  BucketId?: string | null;
  ContentLength?: number | null;
  ContentType?: string | null;
  FileInfo?: string | null;
  UploadTimestamp?: string | null;
  CreatedOn?: string | null;
  CreatedBy?: number | null;
  ModifiedOn?: string | null;
  ModifiedBy?: number | null;
  IsActive?: boolean | null;
}
