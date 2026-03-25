import { Time } from "@angular/common";

export interface Attendence {
  AttendenceId?: number;
  EmployeeId?: number;
  AttendenceDate?: Date;
  CheckInTime?: Time;
  CheckOutTime: Time;
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