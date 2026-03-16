import { Injectable } from "@angular/core";
import { ApiService } from "../../common/services/api.service";
import { Observable } from "rxjs";
import { environment } from "../../../environment";
import { Taskcode } from "../models/taskcode";

@Injectable({
    providedIn: "root"
})
export class TaskcodeService {
    constructor(private apiService: ApiService) { }

    getTaskcodeListAsync(): Observable<any> {
        return this.apiService.send<Taskcode[]>("GET", environment.UrlConstants.Taskcode.GetTaskcodeListAsync);
    }


    deleteTaskcodeAsync(TaskcodeId: number): Observable<any> {
        return this.apiService.send("DELETE", `${environment.UrlConstants.Taskcode.DeleteTaskcodeAsync}/${TaskcodeId}`
        );
    }

    insertOrUpdateStateAsync(taskcode: Taskcode): Observable<Taskcode> {
        return this.apiService.send<Taskcode>("POST", environment.UrlConstants.Taskcode.InsertOrUpdateTaskcodeAsync,taskcode);
    }

}