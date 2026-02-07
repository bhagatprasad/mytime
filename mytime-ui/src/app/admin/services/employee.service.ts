import { Injectable } from "@angular/core";
import { ApiService } from "../../common/services/api.service";
import { Observable } from "rxjs";
import { Employee } from "../models/employee";
import { environment } from "../../../environment";
import { EmployeeDTO } from "../models/employee.dto";

@Injectable({
    providedIn: "root"
})
export class EmployeeService {
    constructor(private apiService: ApiService) { }

    getEmployeesListAsync(): Observable<Employee[]> {
        return this.apiService.send<Employee[]>("GET", environment.UrlConstants.Employee.GetAllEmployees);
    }

    getEmployeeByIdAsync(employeeId: number): Observable<Employee> {
        return this.apiService.send<Employee>("GET", `${environment.UrlConstants.Employee.GetEmployee}/${employeeId}`)
    }

    insertOrUpdateEmployee(employee: EmployeeDTO): Observable<Employee> {
        return this.apiService.send<Employee>("POST", environment.UrlConstants.Employee.InsertOrUpdateEmployee, employee);
    }
}