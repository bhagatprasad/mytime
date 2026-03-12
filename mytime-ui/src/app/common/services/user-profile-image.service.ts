import { Injectable } from "@angular/core";
import { ApiService } from "../../common/services/api.service";
import { Observable } from "rxjs";
import { environment } from "../../../environment";
import { UserProfileImage } from "../models/user-profile-image";


@Injectable({
    providedIn: "root"
})
export class UserProfileImageService {

    constructor(private apiService: ApiService) { }

    fetchAllProfileImagesAsync(): Observable<UserProfileImage[]> {
        return this.apiService.send<UserProfileImage[]>(
            "GET",
            environment.UrlConstants.UserProfileImage.FetchAllProfileImages
        );
    }

    fetchProfileImageByIdAsync(profileImageId: number): Observable<UserProfileImage> {
        return this.apiService.send<UserProfileImage>(
            "GET",
            `${environment.UrlConstants.UserProfileImage.FetchProfileImage}/${profileImageId}`
        );
    }

    fetchProfileImageByUserAsync(userId: number): Observable<UserProfileImage> {
        return this.apiService.send<UserProfileImage>(
            "GET",
            `${environment.UrlConstants.UserProfileImage.FetchProfileImageByUser}/${userId}`
        );
    }

    insertOrUpdateProfileImageAsync(profileImage: Partial<UserProfileImage>): Observable<UserProfileImage> {
        return this.apiService.send<UserProfileImage>(
            "POST",
            environment.UrlConstants.UserProfileImage.InsertOrUpdateProfileImage,
            profileImage
        );
    }

    deleteProfileImageAsync(profileImageId: number): Observable<any> {
        return this.apiService.send<any>(
            "DELETE",
            `${environment.UrlConstants.UserProfileImage.DeleteProfileImage}/${profileImageId}`
        );
    }
}