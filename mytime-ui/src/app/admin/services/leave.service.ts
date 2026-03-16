import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { LeaveType } from '../models/leave-type.model';
import { ApiService } from '../../common/services/api.service';
import { environment } from '../../../environment';
import { Observable } from 'rxjs';


@Injectable({
    providedIn: 'root'
})

export class LeaveService {

    constructor(private apiService: ApiService) { }

    getLeaveTypes(): Observable<LeaveType[]> {
        return this.apiService.send<LeaveType[]>(
            "GET",
            environment.UrlConstants.ApplyLeave.GetleaveTypes
        );
    }

    getAllLeaveRequests(): Observable<any> {
        return this.apiService.send<any>(
            "GET",
            environment.UrlConstants.ApplyLeave.GetAllleaveRequests
        );
    }

    applyLeave(data: any): Observable<any> {
        return this.apiService.send<any>(
            "POST",
            environment.UrlConstants.ApplyLeave.Applyleave,
            data
        );
    }

    getMyLeaves(userId: number): Observable<any> {
        return this.apiService.send<any>(
            "GET",
            `${environment.UrlConstants.ApplyLeave.GetMyLeaves}/${userId}`
        );
    }

    approveLeave(id: number,data: any): Observable<any> {
        return this.apiService.send<any>(
            "PUT",
            `${environment.UrlConstants.ApplyLeave.ApproveLeave}/${id}`,data
        );
    }

    rejectLeave(id: number, data: any): Observable<any> {
        return this.apiService.send<any>(
            "PUT",
            `${environment.UrlConstants.ApplyLeave.RejectLeave}/${id}`,
            data
        );
    }

    cancelLeave(id: number, data: any): Observable<any> {
        return this.apiService.send<any>(
            "PUT",
            `${environment.UrlConstants.ApplyLeave.CancelLeave}/${id}`,
            data
        );
    }

}