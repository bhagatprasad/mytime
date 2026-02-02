import { Injectable } from "@angular/core";
import { ApiService } from "../../common/services/api.service";
import { Observable } from "rxjs";
import { environment } from "../../../environment";
import { EmployeeEmergencyContact } from "../models/employee_emergency_contact";

@Injectable({
    providedIn: "root"
})
export class EmployeeEmergencyContactService {
    constructor(private apiService: ApiService) { }

    // GET methods
    getEmployeeEmergencyContactListAsync(): Observable<EmployeeEmergencyContact[]> {
        return this.apiService.send<EmployeeEmergencyContact[]>("GET", environment.UrlConstants.EmployeeEmergencyContact.GetAllEmployeeEmergencyContacts);
    }

    getEmployeeEmergencyContactByIdAsync(employee_emergency_contact_id: number): Observable<EmployeeEmergencyContact> {
        return this.apiService.send<EmployeeEmergencyContact>("GET", `${environment.UrlConstants.EmployeeEmergencyContact.GetEmployeeEmergencyContact}?employee_emergency_contact_id=${employee_emergency_contact_id}`);
    }

    getEmergencyContactsByEmployeeAsync(employee_id: number): Observable<EmployeeEmergencyContact[]> {
        return this.apiService.send<EmployeeEmergencyContact[]>("GET", `${environment.UrlConstants.EmployeeEmergencyContact.GetContactsByEmployee}?employee_id=${employee_id}`);
    }

    getActiveEmergencyContactsByEmployeeAsync(employee_id: number): Observable<EmployeeEmergencyContact[]> {
        return this.apiService.send<EmployeeEmergencyContact[]>("GET", `${environment.UrlConstants.EmployeeEmergencyContact.GetActiveContactsByEmployee}?employee_id=${employee_id}`);
    }

    getPrimaryEmergencyContactAsync(employee_id: number): Observable<EmployeeEmergencyContact> {
        return this.apiService.send<EmployeeEmergencyContact>("GET", `${environment.UrlConstants.EmployeeEmergencyContact.GetPrimaryEmergencyContact}?employee_id=${employee_id}`);
    }

    getEmployeeEmergencyContactsSummaryAsync(employee_id: number): Observable<any> {
        return this.apiService.send<any>("GET", `${environment.UrlConstants.EmployeeEmergencyContact.GetEmployeeEmergencyContactsSummary}?employee_id=${employee_id}`);
    }

    getEmergencyContactStatisticsAsync(): Observable<any> {
        return this.apiService.send<any>("GET", environment.UrlConstants.EmployeeEmergencyContact.GetEmergencyContactStatistics);
    }

    getEmployeesWithoutEmergencyContactsAsync(): Observable<any[]> {
        return this.apiService.send<any[]>("GET", environment.UrlConstants.EmployeeEmergencyContact.GetEmployeesWithoutEmergencyContacts);
    }

    searchEmergencyContactsByRelationAsync(relation: string): Observable<EmployeeEmergencyContact[]> {
        return this.apiService.send<EmployeeEmergencyContact[]>("GET", `${environment.UrlConstants.EmployeeEmergencyContact.SearchByRelation}?relation=${relation}`);
    }
    // POST methods
    insertOrUpdateEmployeeEmergencyContactAsync(employeeEmergencyContact: EmployeeEmergencyContact): Observable<EmployeeEmergencyContact> {
        return this.apiService.send<EmployeeEmergencyContact>("POST", environment.UrlConstants.EmployeeEmergencyContact.InsertOrUpdateEmployeeEmergencyContact, employeeEmergencyContact);
    }

    createEmployeeEmergencyContactAsync(employeeEmergencyContact: EmployeeEmergencyContact): Observable<EmployeeEmergencyContact> {
        return this.apiService.send<EmployeeEmergencyContact>("POST", environment.UrlConstants.EmployeeEmergencyContact.CreateEmployeeEmergencyContact, employeeEmergencyContact);
    }

    createBulkEmergencyContactsAsync(contacts: EmployeeEmergencyContact[]): Observable<EmployeeEmergencyContact[]> {
        return this.apiService.send<EmployeeEmergencyContact[]>("POST", environment.UrlConstants.EmployeeEmergencyContact.CreateBulkEmergencyContacts, contacts);
    }

    searchEmployeeEmergencyContactsAsync(searchParams: any): Observable<EmployeeEmergencyContact[]> {
        return this.apiService.send<EmployeeEmergencyContact[]>("POST", environment.UrlConstants.EmployeeEmergencyContact.SearchEmployeeEmergencyContacts, searchParams);
    }

    // PUT method
    updateEmployeeEmergencyContactAsync(employee_emergency_contact_id: number, employeeEmergencyContact: EmployeeEmergencyContact): Observable<EmployeeEmergencyContact> {
        return this.apiService.send<EmployeeEmergencyContact>("PUT", `${environment.UrlConstants.EmployeeEmergencyContact.UpdateEmployeeEmergencyContact}?employee_emergency_contact_id=${employee_emergency_contact_id}`, employeeEmergencyContact);
    }

    // DELETE method
    removeEmployeeEmergencyContactAsync(employee_emergency_contact_id: number): Observable<any> {
        return this.apiService.send<any>("DELETE", `${environment.UrlConstants.EmployeeEmergencyContact.DeleteEmployeeEmergencyContact}?employee_emergency_contact_id=${employee_emergency_contact_id}`);
    }
}