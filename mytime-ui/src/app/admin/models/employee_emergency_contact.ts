export interface EmployeeEmergencyContact {
  EmployeeEmergencyContactId: number;
  EmployeeId?: number | null;
  Name?: string | null;
  Relation?: string | null;
  Phone?: string | null;
  Email?: string | null;
  Address?: string | null;
  CreatedOn?: string | null;
  CreatedBy?: number | null;
  ModifiedOn?: string | null;
  ModifiedBy?: number | null;
  IsActive?: boolean | null;
}
