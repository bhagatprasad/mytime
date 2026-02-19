import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { lastValueFrom } from 'rxjs';
import { environment } from '../../../environment';
import { UploadResponse } from '../models/uploadfile_response';
import { DownloadUrlResponse } from '../models/downloadUrl_response';
import { DeleteResponse } from '../models/deletefile_response';

@Injectable({
  providedIn: 'root'
})
export class StorageService {
  private readonly apiBase = environment.baseUrl;
  private readonly urls = environment.UrlConstants.BackblazeUpload;

  constructor(private http: HttpClient) {}

  async uploadFile(file: File, prefix?: string): Promise<UploadResponse> {
    const formData = new FormData();

    const finalFile = prefix
      ? new File([file], `${prefix}_${file.name}`, { type: file.type })
      : file;

    formData.append('file', finalFile);

    const accessToken = localStorage.getItem('AccessToken');
    const headers = new HttpHeaders({
      ...(accessToken ? { 'Authorization': accessToken } : {})
    });

    const url = `${this.apiBase}/${this.urls.UploadEmployeeDocument}`;

    return lastValueFrom(
      this.http.post<UploadResponse>(url, formData, { headers })
    );
  }

  async getDownloadUrl(
    fileId: string,
    expiresIn: number = 3600,
    filename?: string
  ): Promise<DownloadUrlResponse> {
    let params = new HttpParams().set('expires_in', expiresIn.toString());
    if (filename) {
      params = params.set('filename', filename);
    }

    const url = `${this.apiBase}/${this.urls.GetDownloadUrl}/${encodeURIComponent(fileId)}`;

    return lastValueFrom(
      this.http.get<DownloadUrlResponse>(url, { params })
    );
  }

  async deleteFile(fileId: string): Promise<DeleteResponse> {
    const url = `${this.apiBase}/${this.urls.DeleteFile}/${encodeURIComponent(fileId)}`;

    return lastValueFrom(
      this.http.delete<DeleteResponse>(url)
    );
  }
}