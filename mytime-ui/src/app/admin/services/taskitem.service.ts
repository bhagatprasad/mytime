import { Injectable } from "@angular/core";
import { ApiService } from "../../common/services/api.service";
import { Observable } from "rxjs";
import { environment } from "../../../environment";
import { TaskItem } from "../models/taskitem";

@Injectable({
    providedIn: "root"
})
export class TaskitemService {
    constructor(private apiService: ApiService) { }

    GetTaskitemListAsync(): Observable<any> {
        return this.apiService.send<TaskItem[]>("GET", environment.UrlConstants.TaskItem.GetTaskitemListAsync);
    }

    GetTaskitemAsync(TaskItemId: number): Observable<TaskItem> {
        return this.apiService.send<TaskItem>("GET", `${environment.UrlConstants.TaskItem.GetTaskitemAsync}/${TaskItemId}`);
    }


    DeleteTaskItemAsync(TaskItemId: number): Observable<any> {
        return this.apiService.send("DELETE", `${environment.UrlConstants.TaskItem.DeleteTaskItemAsync}/${TaskItemId}`
        );
    }

    InsertOrUpdateTaskItemAsync(TaskItem: TaskItem): Observable<TaskItem> {
        return this.apiService.send<TaskItem>("POST", environment.UrlConstants.TaskItem.InsertOrUpdateTaskItemAsync,TaskItem);
    }

}