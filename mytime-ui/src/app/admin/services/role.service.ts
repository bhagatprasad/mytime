import { Injectable } from "@angular/core";
import { ApiService } from "../../common/services/api.service";
import { Observable } from "rxjs";
import { Role } from "../models/role";
import { environment } from "../../../environment";

@Injectable({ providedIn: 'root' })

export class RoleService {

    constructor(private apiService: ApiService) {

    }

    getRoleListAsync(): Observable<Role[]> {
        return this.apiService.send<Role[]>("GET", environment.UrlConstants.Role.GetRoleListAsync);
    }

}