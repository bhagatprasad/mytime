export interface MonthlySalary {
  MonthlySalaryId : number | null;
  Title: string | null;
  SalaryMonth: string | null;
  SalaryYear: string | null;
  Location: string | null;
  StdDays: number | null;
  WrkDays: number | null;
  LopDays: number | null;
  CreatedOn: Date | null;
  CreatedBy: number | null;
  ModifiedOn: Date | null;
  ModifiedBy: number | null;
  IsActive: boolean | null;
}