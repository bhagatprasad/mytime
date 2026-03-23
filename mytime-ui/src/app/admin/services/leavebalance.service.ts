import { Injectable } from "@angular/core";
import { ApiService } from "../../common/services/api.service";
import { Observable } from "rxjs";
import { LeaveBalance } from "../models/leavebalance";
import { environment } from "../../../environment";

@Injectable({
    providedIn:'root'
})

export class leavebalanceservice{
    constructor(private api:ApiService){}

    getallleavebalanceAsync():Observable<LeaveBalance[]>{
        return this.api.send<LeaveBalance[]>("GET", environment.UrlConstants.leavebalance.GetLeaveBalanceAsync);
    }

    getleavebalancebyuserAsync(id:number):Observable<LeaveBalance>{
        return this.api.send<LeaveBalance>("GET", `${environment.UrlConstants.leavebalance.GetLeaveBalanceByUserAsync}/${id}`);
    }

}