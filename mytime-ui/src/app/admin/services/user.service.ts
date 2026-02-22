import { Injectable } from "@angular/core";
import { ApiService } from "../../common/services/api.service";
import { Observable } from "rxjs";
import { User } from "../models/user";
import { environment } from "../../../environment";
import { RegisterUser } from "../models/register_user";

@Injectable({
    providedIn: "root"
})

export class UserService {

    constructor(private apiService: ApiService) {

    }
    GetAllUsersAsync(): Observable<User[]> {
        return this.apiService.send<User[]>("GET", environment.UrlConstants.Users.GetUsers);
    }
    GetUserByIdAsync(userId: number): Observable<User> {
        return this.apiService.send<User>("GET", `${environment.UrlConstants.Users.GetUserById}/${userId}`);
    }
    RegisterUserAsync(user: RegisterUser): Observable<boolean> {
        return this.apiService.send<boolean>("POST", environment.UrlConstants.Users.RegisterUser, user);
    }
}