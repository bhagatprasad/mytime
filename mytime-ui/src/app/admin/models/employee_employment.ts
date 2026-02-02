export interface EmployeeEmployment {
  EmployeeEmploymentId: number;
  EmployeeId?: number | null;
  
  CompanyName?: string | null;
  Address?: string | null;
  Designation?: string | null;
  
  StartedOn?: string | null;
  EndedOn?: string | null;
  
  Reason?: string | null;
  ReportingManager?: string | null;
  HREmail?: string | null;
  Reference?: string | null;
  
  CreatedOn?: string | null;
  CreatedBy?: number | null;
  
  ModifiedOn?: string | null;
  ModifiedBy?: number | null;
  
  IsActive?: boolean | null;
}
