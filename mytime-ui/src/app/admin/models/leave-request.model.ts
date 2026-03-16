export interface LeaveRequest {

  Id: number;

  UserId?: number;

  LeaveTypeId: number;

  FromDate?: Date;

  ToDate?: Date;

  TotalDays?: number;

  Reason?: string;

  Description?: string;

  Status?: string;

  AdminComment?: string;

  CancelReason?: string;

  CreatedBy?: number;

  CreatedOn?: Date;

  ModifiedBy?: number;

  ModifiedOn?: Date;

  IsActive?: boolean;

}