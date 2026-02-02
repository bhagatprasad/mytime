import { Injectable } from "@angular/core";
import { Observable } from "rxjs";
import { environment } from "../../../environment";
import { ApiService } from "../../common/services/api.service";
import { Designation } from "../models/designation";

@Injectable({
    providedIn: "root"
})

export class DesignationService {

    constructor(private apiService: ApiService) {

    }

    getDesignationsListAsync(): Observable<Designation[]> {
        return this.apiService.send<Designation[]>("GET", environment.UrlConstants.Designation.GetAllDesignations);
    }

    insertOrUpdateDesignation(des: Designation): Observable<Designation> {
        return this.apiService.send<Designation>("POST", environment.UrlConstants.Designation.InsertOrUpdateDesignation, des);
    }

    deleteDesignationAsync(Id: number): Observable<Designation[]> {
            return this.apiService.send<Designation[]>("DELETE", `${environment.UrlConstants.City.GetCitiesByCountry}?DesignationId=${Id}`);
        }

}
