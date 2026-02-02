import { Injectable } from "@angular/core";
import { ApiService } from "../../common/services/api.service";
import { Observable } from "rxjs";
import { environment } from "../../../environment";
import { EmployeeSalaryStructure } from "../models/employee_salary_structure";

@Injectable({
    providedIn: "root"
})
export class EmployeeSalaryStructureService {
    constructor(private apiService: ApiService) { }

    // GET methods
    getEmployeeSalaryStructureListAsync(): Observable<EmployeeSalaryStructure[]> {
        return this.apiService.send<EmployeeSalaryStructure[]>("GET", environment.UrlConstants.EmployeeSalaryStructure.GetAllEmployeeSalaryStructures);
    }

    getEmployeeSalaryStructureByIdAsync(employee_salary_structure_id: number): Observable<EmployeeSalaryStructure> {
        return this.apiService.send<EmployeeSalaryStructure>("GET", `${environment.UrlConstants.EmployeeSalaryStructure.GetEmployeeSalaryStructure}?employee_salary_structure_id=${employee_salary_structure_id}`);
    }

    getSalaryStructureByEmployeeAsync(employee_id: number): Observable<EmployeeSalaryStructure> {
        return this.apiService.send<EmployeeSalaryStructure>("GET", `${environment.UrlConstants.EmployeeSalaryStructure.GetSalaryStructureByEmployee}?employee_id=${employee_id}`);
    }

    getAllSalaryStructuresByEmployeeAsync(employee_id: number): Observable<EmployeeSalaryStructure[]> {
        return this.apiService.send<EmployeeSalaryStructure[]>("GET", `${environment.UrlConstants.EmployeeSalaryStructure.GetAllSalaryStructuresByEmployee}?employee_id=${employee_id}`);
    }

    getActiveSalaryStructuresAsync(): Observable<EmployeeSalaryStructure[]> {
        return this.apiService.send<EmployeeSalaryStructure[]>("GET", environment.UrlConstants.EmployeeSalaryStructure.GetActiveSalaryStructures);
    }

    getSalaryBreakdownAsync(employee_salary_structure_id: number): Observable<any> {
        return this.apiService.send<any>("GET", `${environment.UrlConstants.EmployeeSalaryStructure.GetSalaryBreakdown}?employee_salary_structure_id=${employee_salary_structure_id}`);
    }

    getSalaryStatisticsAsync(): Observable<any> {
        return this.apiService.send<any>("GET", environment.UrlConstants.EmployeeSalaryStructure.GetSalaryStatistics);
    }

    getSalaryComparisonReportAsync(): Observable<any> {
        return this.apiService.send<any>("GET", environment.UrlConstants.EmployeeSalaryStructure.GetSalaryComparisonReport);
    }

    getPayrollSummaryAsync(): Observable<any> {
        return this.apiService.send<any>("GET", environment.UrlConstants.EmployeeSalaryStructure.GetPayrollSummary);
    }

    getEmployeesWithoutSalaryStructureAsync(): Observable<any[]> {
        return this.apiService.send<any[]>("GET", environment.UrlConstants.EmployeeSalaryStructure.GetEmployeesWithoutSalaryStructure);
    }

    calculateNetSalaryAsync(employee_id: number): Observable<any> {
        return this.apiService.send<any>("GET", `${environment.UrlConstants.EmployeeSalaryStructure.CalculateNetSalary}?employee_id=${employee_id}`);
    }

    // POST methods
    insertOrUpdateEmployeeSalaryStructureAsync(employeeSalaryStructure: EmployeeSalaryStructure): Observable<EmployeeSalaryStructure> {
        return this.apiService.send<EmployeeSalaryStructure>("POST", environment.UrlConstants.EmployeeSalaryStructure.InsertOrUpdateEmployeeSalaryStructure, employeeSalaryStructure);
    }

    createEmployeeSalaryStructureAsync(employeeSalaryStructure: EmployeeSalaryStructure): Observable<EmployeeSalaryStructure> {
        return this.apiService.send<EmployeeSalaryStructure>("POST", environment.UrlConstants.EmployeeSalaryStructure.CreateEmployeeSalaryStructure, employeeSalaryStructure);
    }

    searchEmployeeSalaryStructuresAsync(searchParams: any): Observable<EmployeeSalaryStructure[]> {
        return this.apiService.send<EmployeeSalaryStructure[]>("POST", environment.UrlConstants.EmployeeSalaryStructure.SearchEmployeeSalaryStructures, searchParams);
    }

    // PUT method
    updateEmployeeSalaryStructureAsync(employee_salary_structure_id: number, employeeSalaryStructure: EmployeeSalaryStructure): Observable<EmployeeSalaryStructure> {
        return this.apiService.send<EmployeeSalaryStructure>("PUT", `${environment.UrlConstants.EmployeeSalaryStructure.UpdateEmployeeSalaryStructure}?employee_salary_structure_id=${employee_salary_structure_id}`, employeeSalaryStructure);
    }

    // DELETE method
    removeEmployeeSalaryStructureAsync(employee_salary_structure_id: number): Observable<any> {
        return this.apiService.send<any>("DELETE", `${environment.UrlConstants.EmployeeSalaryStructure.DeleteEmployeeSalaryStructure}?employee_salary_structure_id=${employee_salary_structure_id}`);
    }
}