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

    getTaskitemListAsync(): Observable<TaskItem[]> {
        return this.apiService.send<TaskItem[]>("GET", environment.UrlConstants.TaskItem.getTaskitemList);
    }

    getTaskitemAsync(TaskItemId: number): Observable<TaskItem> {
        return this.apiService.send<TaskItem>("GET", `${environment.UrlConstants.TaskItem.getTaskitem}/${TaskItemId}`);
    }


    deleteTaskitemAsync(TaskItemId: number): Observable<any> {
        return this.apiService.send("DELETE", `${environment.UrlConstants.TaskItem.deleteTaskitem}/${TaskItemId}`
        );
    }

    insertOrUpdatetaskitemAsync(TaskItem: TaskItem): Observable<TaskItem> {
        return this.apiService.send<TaskItem>("POST", environment.UrlConstants.TaskItem.insertOrUpdatetaskitem,TaskItem);
    }

}