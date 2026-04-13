import { Injectable } from '@angular/core';
import { ApiService } from '../../common/services/api.service';
import { Observable } from 'rxjs';
import { environment } from '../../../environment';
import { Timesheet } from '../models/timesheet';
import { TimesheetTask } from '../models/timesheet_task';

@Injectable({
  providedIn: 'root',
})
export class TimesheetService {
  constructor(private apiService: ApiService) {}

  getTimesheetsListAsync(): Observable<Timesheet[]> {
    return this.apiService.send<Timesheet[]>(
      'GET',
      environment.UrlConstants.Timesheet.GetAllTimesheets,
    );
  }

  getTimesheetByIdAsync(Id: number): Observable<Timesheet> {
    return this.apiService.send<Timesheet>(
      'GET',
      `${environment.UrlConstants.Timesheet.GetTimesheetById}/${Id}`,
    );
  }

  getTimesheetWithTasksAsync(Id: number): Observable<Timesheet> {
    return this.apiService.send<Timesheet>(
      'GET',
      `${environment.UrlConstants.Timesheet.GetTimesheetWithTasks}/${Id}`,
    );
  }

  getTimesheetsByEmployeeAsync(EmployeeId: number): Observable<Timesheet[]> {
    return this.apiService.send<Timesheet[]>(
      'GET',
      `${environment.UrlConstants.Timesheet.GetTimesheetsByEmployee}/${EmployeeId}`,
    );
  }

  getTimesheetTasksAsync(TimesheetId: number): Observable<TimesheetTask[]> {
    return this.apiService.send<TimesheetTask[]>(
      'GET',
      `${environment.UrlConstants.Timesheet.GetTimesheetTasks}/${TimesheetId}`,
    );
  }

  getTimesheetTaskByIdAsync(Id: number): Observable<TimesheetTask> {
    return this.apiService.send<TimesheetTask>(
      'GET',
      `${environment.UrlConstants.Timesheet.GetTaskById}/${Id}`,
    );
  }

  insertOrUpdateTimesheet(timesheet: Partial<Timesheet>): Observable<any> {
    return this.apiService.send(
      'POST',
      environment.UrlConstants.Timesheet.InsertOrUpdateTimesheet,
      timesheet,
    );
  }

  insertOrUpdateTimesheetTask(task: Partial<TimesheetTask>): Observable<any> {
    return this.apiService.send(
      'POST',
      environment.UrlConstants.Timesheet.InsertOrUpdateTimesheetTask,
      task,
    );
  }

  addTimesheetTask(
    TimesheetId: number,
    task: Partial<TimesheetTask>,
  ): Observable<TimesheetTask> {
    return this.apiService.send<TimesheetTask>(
      'POST',
      `${environment.UrlConstants.Timesheet.AddTimesheetTask}/${TimesheetId}`,
      task,
    );
  }

  deleteTimesheet(Id: number): Observable<void> {
    return this.apiService.send(
      'DELETE',
      `${environment.UrlConstants.Timesheet.DeleteTimesheet}/${Id}`,
    );
  }

  deleteTimesheetTask(Id: number): Observable<void> {
    return this.apiService.send(
      'DELETE',
      `${environment.UrlConstants.Timesheet.DeleteTimesheetTask}/${Id}`,
    );
  }

  approveTimesheet(
    Id: number,
    ApprovedBy: number,
    ApprovedComments?: string,
  ): Observable<any> {
    const data = { Id, ApprovedBy, ApprovedComments };
    return this.apiService.send(
      'POST',
      environment.UrlConstants.Timesheet.ApproveTimesheet,
      data,
    );
  }

  rejectTimesheet(
    Id: number,
    RejectedBy: number,
    RejectedComments?: string,
  ): Observable<any> {
    const data = { Id, RejectedBy, RejectedComments };
    return this.apiService.send(
      'POST',
      environment.UrlConstants.Timesheet.RejectTimesheet,
      data,
    );
  }

  cancelTimesheet(
    Id: number,
    CancelledBy: number,
    CancelledComments?: string,
  ): Observable<any> {
    const data = { Id, CancelledBy, CancelledComments };
    return this.apiService.send(
      'POST',
      environment.UrlConstants.Timesheet.CancelTimesheet,
      data,
    );
  }

  submitTimesheet(Id: number, SubmittedBy: number): Observable<any> {
    const data = { Id, SubmittedBy };
    return this.apiService.send(
      'POST',
      environment.UrlConstants.Timesheet.SubmitTimesheet,
      data,
    );
  }

  updateTimesheetTask(
    Id: number,
    task: Partial<TimesheetTask>,
  ): Observable<TimesheetTask> {
    return this.apiService.send<TimesheetTask>(
      'PUT',
      `${environment.UrlConstants.Timesheet.UpdateTimesheetTask}/${Id}`,
      task,
    );
  }
}
