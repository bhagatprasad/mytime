export interface EmployeeSalaryStructure {
  EmployeeSalaryStructureId: number;
  EmployeeId?: number | null;
  
  PAN?: string | null;
  Adhar?: string | null;
  BankAccount?: string | null;
  BankName?: string | null;
  IFSC?: string | null;
  
  BASIC?: number | null;
  HRA?: number | null;
  CONVEYANCE?: number | null;
  MEDICALALLOWANCE?: number | null;
  SPECIALALLOWANCE?: number | null;
  SPECIALBONUS?: number | null;
  STATUTORYBONUS?: number | null;
  OTHERS?: number | null;
  
  UAN?: string | null;
  PFNO?: string | null;
  
  PF?: number | null;
  ESIC?: number | null;
  PROFESSIONALTAX?: number | null;
  GroupHealthInsurance?: number | null;
  
  GROSSEARNINGS?: number | null;
  GROSSDEDUCTIONS?: number | null;
  
  CreatedBy?: number | null;
  CreatedOn?: string | null;
  ModifiedBy?: number | null;
  ModifiedOn?: string | null;
  
  IsActive?: boolean | null;
}
