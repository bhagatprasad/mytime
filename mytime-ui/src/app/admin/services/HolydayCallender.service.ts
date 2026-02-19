import { Injectable } from "@angular/core";
import { ApiService } from "../../common/services/api.service";
import { Observable } from "rxjs";
import { environment } from "../../../environment";
import { HolidayCallender } from "../models/HolidayCallender";

@Injectable({
    providedIn: "root"
})

export class HolydayCallenderService {
    constructor(private apiService: ApiService) { }

    getHolydaysListAsync(): Observable<HolidayCallender[]> {
        return this.apiService.send<HolidayCallender[]>("GET", environment.UrlConstants.HolidayCalendar.GetAllHolidayCalendars);
    }

    deleteHolydayCallender(Id: number): Observable<void> {
        return this.apiService.send("DELETE", `${environment.UrlConstants.HolidayCalendar.DeleteHolidayCalendar}/${Id}`
        );
    }

    insertOrUpdateHolidayCallender(holiday: HolidayCallender): Observable<HolidayCallender> {
        return this.apiService.send<HolidayCallender>("POST", environment.UrlConstants.HolidayCalendar.InsertOrUpdateHolidayCalendar, holiday);
    }
}