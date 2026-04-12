import { Injectable } from "@angular/core";
import { ApiService } from "../../common/services/api.service";
import { Observable } from "rxjs";
import { EmployeeSalary } from "../models/employee_salary";
import { environment } from "../../../environment";

@Injectable({
    providedIn: 'root'
})

export class EmployeeSalaryService {
    constructor(private apiService: ApiService) { }

    getEmployeeSalaries(): Observable<EmployeeSalary[]> {
        return this.apiService.send<EmployeeSalary[]>("GET", environment.UrlConstants.EmployeeSalary.GetEmployeeSalaries);
    }

    getSalariesByEmployee(employeeId: number): Observable<EmployeeSalary[]> {
        return this.apiService.send<EmployeeSalary[]>("GET", `${environment.UrlConstants.EmployeeSalary.GetSalariesByEmployee}/${employeeId}`);
    }

    getEmployeeSalary(employeeSalaryId: number): Observable<EmployeeSalary> {
        return this.apiService.send<EmployeeSalary>("GET", `${environment.UrlConstants.EmployeeSalary.GetEmployeeSalary}?employeeSalaryId=${employeeSalaryId}`);
    }
}