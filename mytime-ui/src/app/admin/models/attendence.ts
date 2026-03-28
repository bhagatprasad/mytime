export interface Attendence {
  AttendenceId?: number;
  EmployeeId?: number;
  AttendenceDate?: Date;
  CheckInTime?: string;
  CheckOutTime?: string;
  Status?: string;
  WorkHours?: string;
  Description?: string;
  ApprovalStatus?: string;
  CreatedBy?: number;
  CreatedOn?: Date;
  ModifiedBy?: number;
  ModifiedOn?: Date;
  ApprovedBy?: number;
  ApprovedOn?: Date;
  RejectedBy?: number;
  RejectedOn?: Date;
  RejectionReason?: string;
  WorkType?: string;
}