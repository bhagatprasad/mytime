export interface LeaveBalance {
  Id : number;

  UserId : number;

  LeaveTypeId: number;

  Year : Date;
  
  TotalLeaves : number;

  UsedLeaves : number;

  RemainingLeaves : number;

  CreatedBy: number;

  CreatedOn: Date;

  ModifiedBy: number;

  ModifiedOn: Date;

  IsActive: boolean;
}