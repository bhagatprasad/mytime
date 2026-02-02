export interface EmployeeSalary {
  EmployeeSalaryId: number;
  EmployeeId?: number | null;
  MonthlySalaryId?: number | null;
  
  Title?: string | null;
  SalaryMonth?: string | null;
  SalaryYear?: string | null;
  LOCATION?: string | null;
  
  STDDAYS?: number | null;
  WRKDAYS?: number | null;
  LOPDAYS?: number | null;
  
  // Earnings (Monthly / YTD)
  Earning_Monthly_Basic?: number | null;
  Earning_YTD_Basic?: number | null;
  
  Earning_Montly_HRA?: number | null;
  Earning_YTD_HRA?: number | null;
  
  Earning_Montly_CONVEYANCE?: number | null;
  Earning_YTD_CONVEYANCE?: number | null;
  
  Earning_Montly_MEDICALALLOWANCE?: number | null;
  Earning_YTD_MEDICALALLOWANCE?: number | null;
  
  Earning_Montly_SPECIALALLOWANCE?: number | null;
  Earning_YTD_SPECIALALLOWANCE?: number | null;
  
  Earning_Montly_SPECIALBONUS?: number | null;
  Earning_YTD_SPECIALBONUS?: number | null;
  
  Earning_Montly_STATUTORYBONUS?: number | null;
  Earning_YTD_STATUTORYBONUS?: number | null;
  
  Earning_Montly_GROSSEARNINGS?: number | null;
  Earning_YTD_GROSSEARNINGS?: number | null;
  
  Earning_Montly_OTHERS?: number | null;
  Earning_YTD_OTHERS?: number | null;
  
  // Deductions (Monthly / YTD)
  Deduction_Montly_PROFESSIONALTAX?: number | null;
  Deduction_YTD_PROFESSIONALTAX?: number | null;
  
  Deduction_Montly_ProvidentFund?: number | null;
  Deduction_YTD_ProvidentFund?: number | null;
  
  Deduction_Montly_GroupHealthInsurance?: number | null;
  Deduction_YTD_GroupHealthInsurance?: number | null;
  
  Deduction_Montly_OTHERS?: number | null;
  Deduction_YTD_OTHERS?: number | null;
  
  Deduction_Montly_GROSSSDeduction?: number | null;
  Deduction_YTD_GROSSSDeduction?: number | null;
  
  // Net Pay
  NETPAY?: number | null;
  NETTRANSFER?: number | null;
  
  INWords?: string | null;
  
  // Audit
  CreatedOn?: string | null;
  CreatedBy?: number | null;
  ModifiedOn?: string | null;
  ModifiedBy?: number | null;
  
  IsActive?: boolean | null;
}
