export interface Attendence {
  AttendenceId: number;

  EmployeeId: number;
  AttendenceDate: string;

  CheckInTime: string;
  CheckOutTime: string;

  Status: string;
  WorkHours: number;

  Description?: string;

  ApprovalStatus: string;

  CreatedBy: number;
  CreatedOn: string;

  ModifiedBy?: number;
  ModifiedOn?: string;

  ApprovedBy?: number;
  ApprovedOn?: string;

  RejectedBy?: number;
  RejectedOn?: string;

  RejectionReason?: string;
  
  Worktype?: string;
}