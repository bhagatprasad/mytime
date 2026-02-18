import { Injectable } from "@angular/core";
import { ApiService } from "../../common/services/api.service";
import { Observable } from "rxjs";
import { environment } from "../../../environment";
import { EmployeeDocument } from "../models/employee_document";

@Injectable({
    providedIn: "root"
})
export class DocumentService {

    constructor(private apiService: ApiService) { }

    getEmployeeDocumentsAsync(): Observable<EmployeeDocument[]> {
        return this.apiService.send<EmployeeDocument[]>(
            "GET",
            environment.UrlConstants.EmployeeDocuments.GetEmployeeDocuments
        );
    }

    getEmployeeDocumentByIdAsync(employee_document_id: number): Observable<EmployeeDocument> {
        return this.apiService.send<EmployeeDocument>(
            "GET",
            `${environment.UrlConstants.EmployeeDocuments.GetEmployeeDocument}/${employee_document_id}`
        );
    }

    getDocumentsByEmployeeAsync(employee_id: number): Observable<EmployeeDocument[]> {
        return this.apiService.send<EmployeeDocument[]>(
            "GET",
            `${environment.UrlConstants.EmployeeDocuments.GetDocumentsByEmployee}/${employee_id}`
        );
    }

    insertOrUpdateEmployeeDocumentAsync(employeeDocument: EmployeeDocument): Observable<EmployeeDocument> {
        return this.apiService.send<EmployeeDocument>(
            "POST",
            environment.UrlConstants.EmployeeDocuments.InsertOrUpdateEmployeeDocument,
            employeeDocument
        );
    }

    removeEmployeeDocumentAsync(employee_document_id: number): Observable<any> {
        return this.apiService.send<any>(
            "DELETE",
            `${environment.UrlConstants.EmployeeDocuments.DeleteEmployeeDocument}/${employee_document_id}`
        );
    }
}
