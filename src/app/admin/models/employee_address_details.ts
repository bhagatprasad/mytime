import { EmployeeAddress } from "./employee_address";

export interface EmployeeAddressDetails extends EmployeeAddress {
    CountryName: string;
    StateName: string;
    CityName: string;
}