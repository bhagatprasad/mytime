import { Injectable } from "@angular/core";
import { ApiService } from "../../common/services/api.service";
import { Observable } from "rxjs";
import { environment } from "../../../environment";
import { EmployeeEmployment } from "../models/employee_employment";

@Injectable({
    providedIn: "root"
})

export class EmployeeEmploymentService {
    constructor(private apiService: ApiService) { }

    getEmployeeEmployeementListAsyc(): Observable<EmployeeEmployment[]> {
        return this.apiService.send<EmployeeEmployment[]>("GET", environment.UrlConstants.EmployeeEmployment.GetAllEmployeeEmployments);
    }

    getEmploymentsByEmployeeAsync(employeeId: number): Observable<EmployeeEmployment[]> {
        return this.apiService.send<EmployeeEmployment[]>("GET", `${environment.UrlConstants.EmployeeEmployment.GetEmploymentsByEmployee}/${employeeId}`);
    }

    insertOrUpdateEmployementAsync(employeement: EmployeeEmployment): Observable<EmployeeEmployment> {
        return this.apiService.send<EmployeeEmployment>("POST", environment.UrlConstants.EmployeeEmployment.InsertOrUpdateEmployeeEmployment, employeement);
    }

    removeEmployementAsync(employee_employment_id: number): Observable<any> {
        return this.apiService.send<any>("DELETE", `${environment.UrlConstants.EmployeeEmployment.DeleteEmployeeEmployment}?employee_employment_id=${employee_employment_id}`)
    }
}