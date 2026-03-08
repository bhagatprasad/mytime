import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
    providedIn: 'root'
})
export class DirectB2UploadService {
    
    constructor(private http: HttpClient) {}

    /**
     * Ultra-simple upload method - no dependencies on ApiService
     */
    uploadDocument(
        employeeId: number,
        file: File,
        documentType: string,
        description?: string
    ): Observable<any> {
        
        // Create FormData exactly as your backend expects
        const formData = new FormData();
        
        // IMPORTANT: The field names MUST match exactly what's in your FastAPI
        formData.append('file', file);  // parameter name: 'file'
        formData.append('document_type', documentType);  // parameter name: 'document_type'
        
        if (description) {
            formData.append('description', description);  // parameter name: 'description'
        }

        // Log the exact FormData being sent
        console.log('=== FormData Contents ===');
        formData.forEach((value, key) => {
            if (value instanceof File) {
                console.log(`${key}: File(${value.name}, ${value.type}, ${value.size} bytes)`);
            } else {
                console.log(`${key}: ${value}`);
            }
        });

        // Construct the URL exactly as shown in your error
        const url = `https://mytime-docker.onrender.com/api/v1/backblaze/upload-document/${employeeId}`;
        console.log('Upload URL:', url);

        // Make the POST request WITHOUT any headers
        // Let the browser set the correct Content-Type with boundary
        return this.http.post(url, formData);
    }
}