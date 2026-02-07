import { Injectable } from "@angular/core";
import { ApiService } from "../../common/services/api.service";
import { Observable } from "rxjs";
import { City } from "../models/city";
import { environment } from "../../../environment";

@Injectable({
    providedIn: "root"
})
export class CityService {
    constructor(private apiService: ApiService) { }

    getCitiesListAsync(): Observable<City[]> {
        return this.apiService.send<City[]>("GET", environment.UrlConstants.City.GetAllCities);
    }

    getCitiesListByCountryAsync(countryId: number): Observable<City[]> {
        return this.apiService.send<City[]>("GET", `${environment.UrlConstants.City.GetCitiesByCountry}?countryId=${countryId}`);
    }

    getCitiesListByStateAsync(stateId: number): Observable<City[]> {
        return this.apiService.send<City[]>("GET", `${environment.UrlConstants.City.GetCitiesByState}?stateId=${stateId}`);
    }
    getCitiesListByCountryAndStateAsync(countryId: number, stateId: number): Observable<City[]> {
        return this.apiService.send<City[]>("GET", `${environment.UrlConstants.City.GetCitiesByState}?countryId=${countryId}&stateId=${stateId}`);
    }

    deleteCityAsync(Id: number): Observable<void> {
        return this.apiService.send("DELETE", `${environment.UrlConstants.City.DeleteCity}/${Id}`
        );
    }
}