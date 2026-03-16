export interface LeaveHistory {

  id: number;

  leaveRequestId: number;

  status: string;

  comment: string;

  createdBy: number;

  createdOn: Date;

  modifiedBy: number;

  modifiedOn: Date;

  isActive: boolean;

}