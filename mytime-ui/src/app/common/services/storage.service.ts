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
    const formData  = new FormData();
    const finalFile = prefix
      ? new File([file], `${prefix}_${file.name}`, { type: file.type })
      : file;

    formData.append('file', finalFile);

    const url     = `${this.apiBase}/${this.urls.UploadEmployeeDocument}`;
    const headers = await this._authHeaders();

    return lastValueFrom(
      this.http.post<UploadResponse>(url, formData, { headers })
    );
  }

  async getDownloadUrl(
    fileId: string,
    expiresIn = 3600,
    filename?: string
  ): Promise<DownloadUrlResponse> {
    let params = new HttpParams().set('expires_in', expiresIn.toString());
    if (filename) params = params.set('filename', filename);

    const url     = `${this.apiBase}/${this.urls.GetDownloadUrl}/${encodeURIComponent(fileId)}`;
    const headers = await this._authHeaders();

    return lastValueFrom(
      this.http.get<DownloadUrlResponse>(url, { headers, params })
    );
  }

  async deleteFile(fileId: string): Promise<DeleteResponse> {
    const url     = `${this.apiBase}/${this.urls.DeleteFile}/${encodeURIComponent(fileId)}`;
    const headers = await this._authHeaders();

    return lastValueFrom(
      this.http.delete<DeleteResponse>(url, { headers })
    );
  }

  private async _authHeaders(): Promise<HttpHeaders> {
    const token = await lastValueFrom(
      this.store.select(selectToken).pipe(take(1))
    );
    return new HttpHeaders({
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    });
  }
}