import { Injectable } from '@angular/core';
import { HttpClient, HttpBackend, HttpHeaders, HttpParams } from '@angular/common/http';
import { Store } from '@ngrx/store';
import { lastValueFrom } from 'rxjs';
import { take } from 'rxjs/operators';
import { environment } from '../../../environment';
import { UploadResponse } from '../models/uploadfile_response';
import { DownloadUrlResponse } from '../models/downloadUrl_response';
import { DeleteResponse } from '../models/deletefile_response';
import { selectToken } from '../store/auth.selectors';

@Injectable({ providedIn: 'root' })
export class StorageService {

  private readonly apiBase = environment.baseUrl;
  private readonly urls    = environment.UrlConstants.BackblazeUpload;
  private readonly http: HttpClient;

  constructor(
    handler: HttpBackend,
    private readonly store: Store,
  ) {
    this.http = new HttpClient(handler);
  }

  async uploadFile(file: File, prefix?: string): Promise<UploadResponse> {
    try {
      const formData  = new FormData();
      const finalFile = prefix
        ? new File([file], `${prefix}_${file.name}`, { type: file.type })
        : file;

      formData.append('file', finalFile);

      const url     = `${this.apiBase}/${this.urls.UploadEmployeeDocument}`;
      const headers = await this._authHeaders();

      return await lastValueFrom(
        this.http.post<UploadResponse>(url, formData, { headers })
      );
    } catch (error) {
      console.error('Upload failed:', error);
      throw error;
    }
  }

  async getDownloadUrl(
    fileId: string,
    expiresIn = 3600,
    filename?: string
  ): Promise<DownloadUrlResponse> {
    try {
      let params = new HttpParams().set('expires_in', expiresIn.toString());
      if (filename) {
        params = params.set('filename', filename);
      }

      const url = `${this.apiBase}/${this.urls.GetDownloadUrl}/${encodeURIComponent(fileId)}`;
      const headers = await this._authHeaders();

      return await lastValueFrom(
        this.http.get<DownloadUrlResponse>(url, { headers, params })
      );
    } catch (error) {
      console.error('Get download URL failed:', error);
      throw error;
    }
  }

  async deleteFile(fileId: string): Promise<DeleteResponse> {
    try {
      const url = `${this.apiBase}/${this.urls.DeleteFile}/${encodeURIComponent(fileId)}`;
      const headers = await this._authHeaders();

      return await lastValueFrom(
        this.http.delete<DeleteResponse>(url, { headers })
      );
    } catch (error) {
      console.error('Delete failed:', error);
      throw error;
    }
  }

  private async _authHeaders(): Promise<HttpHeaders> {
    try {
      const token = await lastValueFrom(
        this.store.select(selectToken).pipe(take(1))
      );
      
      let headers = new HttpHeaders();
      if (token) {
        headers = headers.set('Authorization', `Bearer ${token}`);
      }
      
      return headers;
    } catch (error) {
      console.error('Failed to get auth token:', error);
      return new HttpHeaders();
    }
  }
}