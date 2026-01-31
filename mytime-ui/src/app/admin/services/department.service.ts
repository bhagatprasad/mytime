import { Injectable } from "@angular/core";
import { ApiService } from "../../common/services/api.service";
import { Observable } from "rxjs";
import { Department } from "../models/department";
import { environment } from "../../../environment";

@Injectable({
    providedIn: "root"
})
export class DepartmentService {

    constructor(private apiService: ApiService) {

    }

    getDepartmentsListAsync(): Observable<Department[]> {
        return this.apiService.send<Department[]>("GET", environment.UrlConstants.Department.GetAllDepartments);
    }

    getDepartmentByIdAsync(departmentId: number): Observable<Department> {
        return this.apiService.send<Department>("GET", `${environment.UrlConstants.Department.GetDepartmentsByIds}?departmentId=${departmentId}`);
    }

    insertOrUpdateDepartmentAsync(department: Department): Observable<Department> {
        return this.apiService.send<Department>("POST", environment.UrlConstants.Department.InsertOrUpdateDepartment, department);
    }
}