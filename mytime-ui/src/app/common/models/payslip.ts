import { Department } from "../../admin/models/department";
import { Designation } from "../../admin/models/designation";
import { Employee } from "../../admin/models/employee";
import { EmployeeSalary } from "../../admin/models/employee_salary";
import { EmployeeSalaryStructure } from "../../admin/models/employee_salary_structure";

export interface PayslipVM {
  employee?: Employee;
  employeeSalary?: EmployeeSalary;
  department?: Department;
  designation?: Designation;
  employeeSalaryStructure?: EmployeeSalaryStructure;
}