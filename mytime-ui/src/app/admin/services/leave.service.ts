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

    GetleaveTypesAsync(): Observable<LeaveType[]> {
        return this.apiService.send<LeaveType[]>(
            "GET",
            environment.UrlConstants.ApplyLeave.GetleaveTypesAsync
        );
    }

    GetAllleaveRequestsAsync(): Observable<any> {
        return this.apiService.send<any>(
            "GET",
            environment.UrlConstants.ApplyLeave.GetAllleaveRequestsAsync
        );
    }

    ApplyleaveAsync(data: any): Observable<any> {
        return this.apiService.send<any>(
            "POST",
            environment.UrlConstants.ApplyLeave.ApplyleaveAsync,
            data
        );
    }

    GetMyLeavesAsync(userId: any): Observable<any> {
        return this.apiService.send<any>(
            "GET",
            `${environment.UrlConstants.ApplyLeave.GetMyLeavesAsync}/${userId}`
        );
    }

    ApproveLeaveAsync(id: number,data: any): Observable<any> {
        return this.apiService.send<any>(
            "PUT",
            `${environment.UrlConstants.ApplyLeave.ApproveLeaveAsync}/${id}`,data
        );
    }

    RejectLeaveAsync(id: number, data: any): Observable<any> {
        return this.apiService.send<any>(
            "PUT",
            `${environment.UrlConstants.ApplyLeave.RejectLeaveAsync}/${id}`,
            data
        );
    }

    CancelLeaveAsync(id: number, data: any): Observable<any> {
        return this.apiService.send<any>(
            "PUT",
            `${environment.UrlConstants.ApplyLeave.CancelLeaveAsync}/${id}`,
            data
        );
    }

}