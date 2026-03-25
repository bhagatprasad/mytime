import { Injectable } from "@angular/core";
import { ApiService } from "../../common/services/api.service";
import { Observable } from "rxjs";
import { Attendence } from "../models/attendence";
import { environment } from "../../../environment";

@Injectable({
  providedIn: "root"
})
export class AttendenceService {

  constructor(private apiService: ApiService) { }

  getAttendenceListAsync(): Observable<Attendence[]> {
    return this.apiService.send<Attendence[]>(
      "GET",
      environment.UrlConstants.Attendence.GetAllAttendence
    );
  }

  getAttendenceListByEmployeeAsync(employeeId: number): Observable<Attendence[]> {
    return this.apiService.send<Attendence[]>(
      "GET",
      `${environment.UrlConstants.Attendence.GetAllAttendenceByEmployee}/${employeeId}`
    );
  }

  getAttendenceByIdAsync(id: number): Observable<Attendence> {
    return this.apiService.send<Attendence>(
      "GET",
      `${environment.UrlConstants.Attendence.GetAttendenceById}/${id}`
    );
  }
  insertOrUpdateAttendence(attendence: Attendence): Observable<Attendence> {
    return this.apiService.send<Attendence>(
      "POST",
      environment.UrlConstants.Attendence.InsertOrUpdateAttendence,
      attendence
    );
  }
  deleteAttendence(attendenceId: number): Observable<void> {
    return this.apiService.send<void>(
      "DELETE",
      `${environment.UrlConstants.Attendence.DeleteAttendence}/${attendenceId}`
    );
  }
  approveAttendence(attendenceId: number, approvedBy: number): Observable<Attendence> {
    return this.apiService.send<Attendence>(
      "PUT",
      `${environment.UrlConstants.Attendence.ApproveAttendence}/${attendenceId}`,
      { ApprovedBy: approvedBy }
    );
  }
  rejectAttendence(attendenceId: number, rejectedBy: number, reason: string): Observable<Attendence> {
    return this.apiService.send<Attendence>(
      "PUT",
      `${environment.UrlConstants.Attendence.RejectAttendence}/${attendenceId}`,
      {
        RejectedBy: rejectedBy,
        RejectionReason: reason
      }
    );
  }
  getAttendenceByEmployeeAsync(employeeId: number): Observable<Attendence[]> {
    return this.apiService.send<Attendence[]>(
      "GET",
      `${environment.UrlConstants.Attendence.GetAttendenceByEmployee}/${employeeId}`
    );
  }

  getAttendenceByDateAsync(date: string): Observable<Attendence[]> {
    return this.apiService.send<Attendence[]>(
      "GET",
      `${environment.UrlConstants.Attendence.GetAttendenceByDate}/${date}`
    );
  }
}