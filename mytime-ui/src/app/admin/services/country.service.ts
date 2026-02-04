import { Injectable } from "@angular/core";
import { ApiService } from "../../common/services/api.service";
import { Observable } from "rxjs";
import { Country } from "../models/country";
import { environment } from "../../../environment";

@Injectable({
    providedIn: "root"
})

export class CountryService {

    constructor(private apiService: ApiService) { }

    getCountriesListAsync(): Observable<Country[]> {
        return this.apiService.send<Country[]>("GET", environment.UrlConstants.Country.GetAllCountries);
    }

    insertOrUpdateCountry(country: Country): Observable<Country> {
        return this.apiService.send<Country>("POST", environment.UrlConstants.Country.InsertOrUpdateCountry, country);
    }

    deleteCountry(countryId: number): Observable<void> {
        return this.apiService.send("DELETE", `${environment.UrlConstants.Country.DeleteCountry}/${countryId}`
        );
    }
}