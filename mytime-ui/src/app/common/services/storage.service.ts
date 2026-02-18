import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from '../../../environment';
import { B2UploadOptions } from '../models/b2Upload-options';
import { B2UploadResponse } from '../models/b2Upload_response';
import { lastValueFrom } from 'rxjs';

@Injectable({
    providedIn: 'root'
})
export class StorageService {
    private authToken: string = '';
    private apiUrl: string = '';
    private uploadUrl: string = '';
    private uploadAuthToken: string = '';

    private readonly B2_KEY_ID = environment.UrlConstants.Backblaze.keyId;
    private readonly B2_APP_KEY = environment.UrlConstants.Backblaze.applicationKey;
    private readonly B2_BUCKET_ID = environment.UrlConstants.Backblaze.bucketId;
    private readonly B2_BUCKET_NAME = environment.UrlConstants.Backblaze.bucketName;
    private readonly B2_ENDPOINT = environment.UrlConstants.Backblaze.endpoint;

    constructor(private http: HttpClient) { }

    private async authorize(): Promise<void> {
        try {
            const authString = btoa(`${this.B2_KEY_ID}:${this.B2_APP_KEY}`);

            const headers = new HttpHeaders({
                'Authorization': `Basic ${authString}`,
                'Accept': 'application/json'
            });

            console.log('Calling authorize via proxy...');

            const response: any = await lastValueFrom(
                this.http.get('/api/b2api/v2/b2_authorize_account', {
                    headers,
                    responseType: 'json'
                })
            );

            console.log('Authorization successful:', response);
            this.apiUrl = response.apiUrl;
            this.authToken = response.authorizationToken;

        } catch (error) {
            console.error('Authorization failed:', error);
            throw error;
        }
    }

    private async getUploadUrl(): Promise<void> {
        const headers = new HttpHeaders({
            'Authorization': this.authToken
        });

        // This can stay as is because it uses the apiUrl from the authorize response
        const response: any = await lastValueFrom(
            this.http.post(`${this.apiUrl}/b2api/v2/b2_get_upload_url`,
                { bucketId: this.B2_BUCKET_ID },
                { headers }
            )
        );

        this.uploadUrl = response.uploadUrl;
        this.uploadAuthToken = response.authorizationToken;
    }

    async uploadFile(file: File, options?: B2UploadOptions): Promise<B2UploadResponse> {
        try {
            if (!this.authToken) {
                await this.authorize();
            }

            if (!this.uploadUrl) {
                await this.getUploadUrl();
            }

            const fileData = await this.readFileAsArrayBuffer(file);

            const sha1 = await this.calculateSHA1(fileData);

            let headers = new HttpHeaders({
                'Authorization': this.uploadAuthToken,
                'X-Bz-File-Name': encodeURIComponent(options?.fileName || file.name),
                'Content-Type': options?.mime || file.type || 'b2/x-auto',
                'X-Bz-Content-Sha1': sha1
            });

            if (options?.fileInfo) {
                Object.keys(options.fileInfo).forEach(key => {
                    headers = headers.set(`X-Bz-Info-${key}`, String(options.fileInfo![key]));
                });
            }

            const uploadResponse: any = await lastValueFrom(
                this.http.post(this.uploadUrl, fileData, { headers })
            );

            return this.formatUploadResponse(uploadResponse);

        } catch (error) {
            this.resetAuth();
            console.error('B2 upload failed:', error);
            throw this.handleError(error);
        }
    }

    private calculateSHA1(buffer: ArrayBuffer): Promise<string> {
        return crypto.subtle.digest('SHA-1', buffer).then(hashBuffer => {
            const hashArray = Array.from(new Uint8Array(hashBuffer));
            const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
            return hashHex;
        });
    }

    private readFileAsArrayBuffer(file: File): Promise<ArrayBuffer> {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = () => resolve(reader.result as ArrayBuffer);
            reader.onerror = reject;
            reader.readAsArrayBuffer(file);
        });
    }

    private formatUploadResponse(response: any): B2UploadResponse {
        return {
            fileId: response.fileId,
            fileName: decodeURIComponent(response.fileName),
            bucketId: response.bucketId,
            contentLength: response.contentLength,
            contentType: response.contentType,
            contentSha1: response.contentSha1,
            fileInfo: {},
            uploadTimestamp: response.uploadTimestamp,
            action: response.action
        };
    }

    private resetAuth(): void {
        this.authToken = '';
        this.apiUrl = '';
        this.uploadUrl = '';
        this.uploadAuthToken = '';
    }

    private handleError(error: any): Error {
        if (error.error && error.error.message) {
            return new Error(`B2 API Error: ${error.error.message}`);
        } else if (error.message) {
            return new Error(`Upload Error: ${error.message}`);
        } else {
            return new Error('Unknown upload error occurred');
        }
    }

    getPublicUrl(fileName: string): string {
        return `https://${this.B2_BUCKET_NAME}.${this.B2_ENDPOINT}/${fileName}`;
    }

    async getAuthorizedUrl(fileName: string, expiresInSeconds: number = 3600): Promise<string> {
        try {
            if (!this.authToken) {
                await this.authorize();
            }

            const headers = new HttpHeaders({
                'Authorization': this.authToken
            });

            const response: any = await lastValueFrom(
                this.http.post(`${this.apiUrl}/b2api/v2/b2_get_download_authorization`, {
                    bucketId: this.B2_BUCKET_ID,
                    fileNamePrefix: fileName,
                    validDurationInSeconds: expiresInSeconds
                }, { headers })
            );

            return `https://${this.B2_BUCKET_NAME}.${this.B2_ENDPOINT}/${fileName}?Authorization=${response.authorizationToken}`;
        } catch (error) {
            console.error('Failed to get authorized URL:', error);
            throw error;
        }
    }

    async deleteFile(fileName: string, fileId: string): Promise<void> {
        try {
            if (!this.authToken) {
                await this.authorize();
            }

            const headers = new HttpHeaders({
                'Authorization': this.authToken
            });

            await lastValueFrom(
                this.http.post(`${this.apiUrl}/b2api/v2/b2_delete_file_version`, {
                    fileName: fileName,
                    fileId: fileId
                }, { headers })
            );
        } catch (error) {
            console.error('Failed to delete file:', error);
            throw error;
        }
    }

    async listFiles(prefix?: string, limit: number = 100): Promise<any> {
        try {
            if (!this.authToken) {
                await this.authorize();
            }

            const headers = new HttpHeaders({
                'Authorization': this.authToken
            });

            const response: any = await lastValueFrom(
                this.http.post(`${this.apiUrl}/b2api/v2/b2_list_file_names`, {
                    bucketId: this.B2_BUCKET_ID,
                    prefix: prefix || '',
                    maxFileCount: limit
                }, { headers })
            );

            return response;
        } catch (error) {
            console.error('Failed to list files:', error);
            throw error;
        }
    }

    validateFileSize(file: File, maxSizeMB: number = 100): boolean {
        const maxSizeBytes = maxSizeMB * 1024 * 1024;
        return file.size <= maxSizeBytes;
    }

    validateFileType(file: File, allowedTypes: string[]): boolean {
        return allowedTypes.includes(file.type);
    }
}