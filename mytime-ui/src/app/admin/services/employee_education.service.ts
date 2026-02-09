
import { Injectable } from "@angular/core";
import { ApiService } from "../../common/services/api.service";
import { Observable } from "rxjs";
import { environment } from "../../../environment";
import { EmployeeEducation } from "../models/employee_education";


@Injectable({
    providedIn: "root"
})

export class EmployeeEducationService {
    constructor(private apiService: ApiService) { }

    getEmployeementEducationsListAsync(): Observable<EmployeeEducation[]> {
        return this.apiService.send<EmployeeEducation[]>("GET", environment.UrlConstants.EmployeeEducation.GetAllEmployeeEducations);
    }

    getEmployeeEducationsListAsync(employeeId: any): Observable<EmployeeEducation[]> {
        return this.apiService.send<EmployeeEducation[]>("GET", `${environment.UrlConstants.EmployeeEducation.GetEducationsByEmployee}/${employeeId}`);
    }

    insertOrUpdateEmployeeEducationAsync(employee_education: EmployeeEducation): Observable<EmployeeEducation> {
        return this.apiService.send<EmployeeEducation>("POST", environment.UrlConstants.EmployeeEducation.InsertOrUpdateEmployeeEducation, employee_education);
    }

    removeEmployeeEducation(employee_education_id: number): Observable<any> {
        return this.apiService.send<any>("DELETE", `${environment.UrlConstants.EmployeeEducation.DeleteEmployeeEducation}?employee_education_id  =${employee_education_id}`)
    }
}