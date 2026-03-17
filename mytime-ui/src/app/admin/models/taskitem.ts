export interface TaskItem {
    TaskItemId: number;
    Name: string;
    Code: string;
    CreatedBy?: number;
    CreatedOn?: Date;
    ModifiedBy?: number;
    ModifiedOn?: Date;
    IsActive?: boolean;
    ProjectId?: number;
}