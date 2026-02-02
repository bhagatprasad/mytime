export interface EmployeeDocument {
  Id: number;
  EmployeeId: number;
  DocumentTypeId: number;
  DocumentName?: string | null;
  DocumentPath?: string | null;
  DocumentExtension?: string | null;
  CreatedBy?: number | null;
  CreatedOn?: string | null;
  ModifiedBy?: number | null;
  ModifiedOn?: string | null;
  IsActive?: boolean | null;
}
