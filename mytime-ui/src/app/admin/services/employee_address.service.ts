import { Injectable } from "@angular/core";
import { ApiService } from "../../common/services/api.service";
import { Observable } from "rxjs";
import { environment } from "../../../environment";
import { EmployeeAddress } from "../models/employee_address";

@Injectable({
    providedIn: "root"
})

export class EmployeeAddressService {
    constructor(private apiService: ApiService) { }

    getEmployeeAddressListAsync(): Observable<EmployeeAddress[]> {
        return this.apiService.send<EmployeeAddress[]>("GET", environment.UrlConstants.EmployeeAddress.GetAllEmployeeAddresses);
    }

    getEmployeeAddressListByEmployeeAsync(employee_id: number): Observable<EmployeeAddress[]> {
        return this.apiService.send<EmployeeAddress[]>("GET", `${environment.UrlConstants.EmployeeAddress.GetAddressesByEmployee}?employee_id=${employee_id}`);
    }
    insertOrUpdateEmployeeAddressAsync(employeeAddress: EmployeeAddress): Observable<EmployeeAddress> {
        return this.apiService.send<EmployeeAddress>("POST", environment.UrlConstants.EmployeeAddress.InsertOrUpdateEmployeeAddress, employeeAddress);
    }
    removeEmployeeAddressAsync(employee_address_id: number): Observable<any> {
        return this.apiService.send<any>("DELETE", `${environment.UrlConstants.EmployeeAddress.DeleteEmployeeAddress}?employee_address_id=${employee_address_id}`)
    }
}