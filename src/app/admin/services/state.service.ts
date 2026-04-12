import { Injectable } from "@angular/core";
import { ApiService } from "../../common/services/api.service";
import { Observable } from "rxjs";
import { State } from "../models/state";
import { environment } from "../../../environment";

@Injectable({
    providedIn: "root"
})
export class StateService {
    constructor(private apiService: ApiService) {

    }

    getStateListAsync(): Observable<State[]> {
        return this.apiService.send<State[]>("GET", environment.UrlConstants.State.GetAllStates);
    }

    getStatesByCountry(countryId: number): Observable<State[]> {
  return this.apiService.send<State[]>(
    "GET",
    environment.UrlConstants.State.GetStatesByCountry + countryId
  );
}


    deleteStateAsync(stateId: number): Observable<any> {
        return this.apiService.send("DELETE", `${environment.UrlConstants.State.DeleteState}/${stateId}`
        );
    }

    insertOrUpdateStateAsync(state: State): Observable<State> {
        return this.apiService.send<State>("POST", environment.UrlConstants.State.InsertOrUpdateState, state);
    }
}