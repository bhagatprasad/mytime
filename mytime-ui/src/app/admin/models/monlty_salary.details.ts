import { EmployeeSalary } from "./employee_salary";
import { MonthlySalary } from "./monlty_salary";

export interface MonthlySalaryDetails extends MonthlySalary {
     employee_salaries: EmployeeSalary[];
    total_employees: number;
}