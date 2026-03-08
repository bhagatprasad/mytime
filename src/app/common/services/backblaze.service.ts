import { Injectable } from "@angular/core";
import { HttpClient, HttpHeaders, HttpRequest } from "@angular/common/http";
import { Observable, throwError } from "rxjs";
import { catchError, tap } from "rxjs/operators";
import { environment } from "../../../environment";
import { ApiService } from "./api.service";

@Injectable({
    providedIn: "root"
})
export class BackBlazeService {

    constructor(
        private http: HttpClient,
        // Keep apiService for non-file operations if needed
        private apiService: ApiService
    ) { }

    /**
     * Upload file directly using HttpClient (bypassing ApiService for FormData)
     */
    uploadEmployeeDocumentAsync(
        employeeId: number,
        file: File,
        documentType: string,
        description?: string
    ): Observable<any> {

        // Validate employee ID
        if (!employeeId || employeeId <= 0) {
            return throwError(() => new Error('Invalid employee ID'));
        }

        const formData = new FormData();
        
        // IMPORTANT: The field names must match exactly what FastAPI expects
        formData.append("file", file, file.name);  // Field name: 'file'
        formData.append("document_type", documentType);  // Field name: 'document_type'

        if (description && description.trim()) {
            formData.append("description", description.trim());  // Field name: 'description'
        }

        // Log FormData contents for debugging
        console.log('Uploading to employee ID:', employeeId);
        console.log('FormData contents:');
        formData.forEach((value, key) => {
            if (value instanceof File) {
                console.log(`- ${key}: File(name=${value.name}, type=${value.type}, size=${value.size})`);
            } else {
                console.log(`- ${key}: ${value}`);
            }
        });

        // Construct the full URL
        const url = `${environment.baseUrl}/${environment.UrlConstants.BackblazeUpload.UploadEmployeeDocument}/${employeeId}`;
        console.log('Full URL:', url);

        // Use HttpClient directly for the upload
        return this.http.post<any>(url, formData, {
            // Don't set Content-Type header - let browser set it with boundary
            headers: new HttpHeaders({
                // Remove any default headers that might cause issues
                // 'Content-Type' is intentionally omitted
            }),
            // Optional: Add progress reporting
            reportProgress: true,
            // Observe the full response if you need headers
            observe: 'body'
        }).pipe(
            tap(response => console.log('Upload successful:', response)),
            catchError(error => {
                console.error('Upload failed:', error);
                
                if (error.status === 422) {
                    console.error('Validation error details:', error.error);
                    console.error('This usually means the field names in FormData do not match what FastAPI expects');
                }
                
                return throwError(() => error);
            })
        );
    }

    /**
     * Get download URL - can use ApiService since it's a GET request
     */
    getDownloadUrlAsync(fileName: string, expiresIn?: number): Observable<any> {
        let url = `${environment.UrlConstants.BackblazeUpload.GetDownloadUrl}/${encodeURIComponent(fileName)}`;
        
        if (expiresIn) {
            url += `?expires_in=${expiresIn}`;
        }

        // Use apiService for non-file operations
        return this.apiService.send<any>("GET", url).pipe(
            catchError(error => {
                console.error('Failed to get download URL:', error);
                return throwError(() => error);
            })
        );
    }

    /**
     * Delete file - can use ApiService
     */
    deleteFileAsync(fileName: string, employeeDocumentId: number): Observable<any> {
        if (!employeeDocumentId || employeeDocumentId <= 0) {
            return throwError(() => new Error('Invalid employee document ID'));
        }

        const url = `${environment.UrlConstants.BackblazeUpload.DeleteFile}/${encodeURIComponent(fileName)}/${employeeDocumentId}`;
        
        return this.apiService.send<any>("DELETE", url).pipe(
            catchError(error => {
                console.error('Failed to delete file:', error);
                return throwError(() => error);
            })
        );
    }

    /**
     * Get file info - can use ApiService
     */
    getFileInfoAsync(fileName: string): Observable<any> {
        const url = `${environment.UrlConstants.BackblazeUpload.GetFileInfo}/${encodeURIComponent(fileName)}`;
        
        return this.apiService.send<any>("GET", url).pipe(
            catchError(error => {
                console.error('Failed to get file info:', error);
                return throwError(() => error);
            })
        );
    }

    /**
     * Get bucket stats - can use ApiService
     */
    getBucketStatsAsync(): Observable<any> {
        return this.apiService.send<any>("GET", environment.UrlConstants.BackblazeUpload.GetBucketStats).pipe(
            catchError(error => {
                console.error('Failed to get bucket stats:', error);
                return throwError(() => error);
            })
        );
    }

    /**
     * List files - can use ApiService
     */
    listFilesAsync(prefix?: string, employeeId?: number, limit: number = 100): Observable<any> {
        let url = environment.UrlConstants.BackblazeUpload.ListFiles;
        const params: string[] = [];
        
        if (prefix) {
            params.push(`prefix=${encodeURIComponent(prefix)}`);
        }
        if (employeeId) {
            params.push(`employee_id=${employeeId}`);
        }
        if (limit !== 100) {
            params.push(`limit=${limit}`);
        }
        
        if (params.length > 0) {
            url += '?' + params.join('&');
        }

        return this.apiService.send<any>("GET", url).pipe(
            catchError(error => {
                console.error('Failed to list files:', error);
                return throwError(() => error);
            })
        );
    }

    /**
     * Helper method to validate file before upload
     */
    validateFileForUpload(file: File, maxSizeMB: number = 100): { valid: boolean; error?: string } {
        // Check file size (default 100MB)
        const maxSizeBytes = maxSizeMB * 1024 * 1024;
        if (file.size > maxSizeBytes) {
            return {
                valid: false,
                error: `File size exceeds ${maxSizeMB}MB limit`
            };
        }

        // Check if file is empty
        if (file.size === 0) {
            return {
                valid: false,
                error: 'File is empty'
            };
        }

        // Optional: Check file type
        const allowedTypes = ['image/jpeg', 'image/png', 'application/pdf', 'image/jpg'];
        if (!allowedTypes.includes(file.type)) {
            return {
                valid: false,
                error: 'File type not allowed. Please upload JPEG, PNG, or PDF files.'
            };
        }

        return { valid: true };
    }

    /**
     * Alternative upload method with progress tracking
     */
    uploadEmployeeDocumentWithProgress(
        employeeId: number,
        file: File,
        documentType: string,
        description?: string
    ): Observable<any> {
        if (!employeeId || employeeId <= 0) {
            return throwError(() => new Error('Invalid employee ID'));
        }

        const formData = new FormData();
        formData.append("file", file, file.name);
        formData.append("document_type", documentType);

        if (description && description.trim()) {
            formData.append("description", description.trim());
        }

        const url = `${environment.baseUrl}/${environment.UrlConstants.BackblazeUpload.UploadEmployeeDocument}/${employeeId}`;

        // Create a request with progress events
        const req = new HttpRequest('POST', url, formData, {
            reportProgress: true,
            // Don't set Content-Type header
        });

        return this.http.request(req).pipe(
            catchError(error => {
                console.error('Upload failed:', error);
                return throwError(() => error);
            })
        );
    }
}