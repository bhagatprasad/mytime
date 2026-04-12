import { TimesheetTask } from "./timesheet_task";

export interface Timesheet {
  Id?: number;
  FromDate?: Date | string;
  ToDate?: Date | string;
  Description?: string;
  EmployeeId?: number;
  UserId?: number;
  Status?: string;
  AssignedOn?: Date | string;
  AssignedTo?: number;
  ApprovedOn?: Date | string;
  ApprovedBy?: number;
  ApprovedComments?: string;
  CancelledOn?: Date | string;
  CancelledBy?: number;
  CancelledComments?: string;
  RejectedOn?: Date | string;
  RejectedBy?: number;
  RejectedComments?: string;
  TotalHrs?: number;
  CreatedBy?: number;
  CreatedOn?: Date | string;
  ModifiedBy?: number;
  ModifiedOn?: Date | string;
  IsActive?: boolean;
  Tasks?: TimesheetTask[];
}