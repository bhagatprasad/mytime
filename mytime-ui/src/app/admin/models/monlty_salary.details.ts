import { EmployeeSalary } from "./employee_salary";
import { MonthlySalary } from "./monlty_salary";

export interface MonthlySalaryDetails extends MonthlySalary {
    employeesalaries: EmployeeSalary[];
    total_employees: number;
}