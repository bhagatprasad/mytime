export interface TimesheetTask {
  Id?: number;
  TimesheetId?: number;
  TaskItemId?: number;
  TaskCodeId?: number;
  MondayHours?: number;
  TuesdayHours?: number;
  WednesdayHours?: number;
  ThursdayHours?: number;
  FridayHours?: number;
  SaturdayHours?: number;
  SundayHours?: number;
  TotalHrs?: number;
  CreatedBy?: number;
  CreatedOn?: Date | string;
  ModifiedBy?: number;
  ModifiedOn?: Date | string;
  IsActive?: boolean;
}
