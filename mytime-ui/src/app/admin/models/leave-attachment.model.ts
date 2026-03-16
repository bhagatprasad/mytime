export interface LeaveAttachment {

  id: number;

  leaveRequestId: number;

  fileName: string;

  filePath: string;

  fileType: string;

  createdBy: number;

  createdOn: Date;

  modifiedBy: number;

  modifiedOn: Date;

  isActive: boolean;

}