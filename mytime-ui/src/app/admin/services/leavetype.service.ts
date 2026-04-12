import { Injectable } from '@angular/core';
import { ApiService } from '../../common/services/api.service';
import { Observable } from 'rxjs';
import { LeaveType } from '../models/leave-type.model';
import { environment } from '../../../environment';

@Injectable({
  providedIn: 'root',
})
export class LeaveTypeService {
  constructor(private apiService: ApiService) {}

  GetleaveTypeAsync(): Observable<LeaveType[]> {
    return this.apiService.send<LeaveType[]>(
      'GET',
      environment.UrlConstants.LeaveType.GetLeaveTypeAsync,
    );
  }

  InsertOrUpdateLeaveTypeAsync(leavetype: LeaveType): Observable<any> {
    return this.apiService.send<any>(
      'POST',
      environment.UrlConstants.LeaveType.InsertOrUpdateLeaveTypeAsync,
      leavetype,
    );
  }

  DeleteLeaveTypeAsync(leavetypeId: number): Observable<any> {
    return this.apiService.send<any>(
      'DELETE',
      `${environment.UrlConstants.LeaveType.DeleteLeaveTypeAsync}/${leavetypeId}`,
    );
  }

  GetLeaveTypeExistsAsync(): Observable<LeaveType[]> {
    return this.apiService.send<LeaveType[]>(
      'GET',
      environment.UrlConstants.LeaveType.GetLeaveTypeExistsAsync,
    );
  }

  GetLeaveTypeNameAsync(): Observable<LeaveType[]> {
    return this.apiService.send<LeaveType[]>(
      'GET',
      environment.UrlConstants.LeaveType.GetLeaveTypeNameAsync,
    );
  }

  GetLeaveTypeListAsync(): Observable<LeaveType[]> {
    return this.apiService.send<LeaveType[]>(
      'GET',
      environment.UrlConstants.LeaveType.GetLeaveTypeListAsync,
    );
  }
}
