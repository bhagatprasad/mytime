import { Employee } from "./employee";

export interface EmployeesDetails extends Employee {
    DeparmtnetName: string;
    DesignationName: string;
    RoleName: string;
}