import { Injectable } from '@angular/core';
import { HttpClient, HttpBackend, HttpHeaders, HttpParams } from '@angular/common/http';
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
  
  private readonly http: HttpClient;

  constructor(handler: HttpBackend) {
    this.http = new HttpClient(handler);
  }

  private getAuthHeaders(): HttpHeaders {
    const accessToken = localStorage.getItem('AccessToken');
    return new HttpHeaders({
      ...(accessToken ? { 'Authorization': accessToken } : {})
    });
  }

  async uploadFile(file: File, prefix?: string): Promise<UploadResponse> {
    const formData = new FormData();

    const finalFile = prefix
      ? new File([file], `${prefix}_${file.name}`, { type: file.type })
      : file;

    formData.append('file', finalFile);

    const url = `${this.apiBase}/${this.urls.UploadEmployeeDocument}`;

    return lastValueFrom(
      this.http.post<UploadResponse>(url, formData, { headers: this.getAuthHeaders() })
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
      this.http.get<DownloadUrlResponse>(url, { headers: this.getAuthHeaders(), params })
    );
  }

  async deleteFile(fileId: string): Promise<DeleteResponse> {
    const url = `${this.apiBase}/${this.urls.DeleteFile}/${encodeURIComponent(fileId)}`;

    return lastValueFrom(
      this.http.delete<DeleteResponse>(url, { headers: this.getAuthHeaders() })
    );
  }
}