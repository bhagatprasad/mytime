export interface EmployeeEducation {
  EmployeeEducationId: number;
  EmployeeId?: number | null;
  Degree?: string | null;
  FeildOfStudy?: string | null;
  Institution?: string | null;
  YearOfCompletion?: Date | null;
  PercentageMarks?: string | null;
  CreatedOn?: string | null;
  CreatedBy?: number | null;
  ModifiedOn?: string | null;
  ModifiedBy?: number | null;
  IsActive?: boolean | null;
}
