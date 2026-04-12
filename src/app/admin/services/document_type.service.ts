import { Injectable } from '@angular/core';
import { ApiService } from '../../common/services/api.service';
import { Observable } from 'rxjs';
import { DocumentType } from '../models/document_type';
import { environment } from '../../../environment';

@Injectable({
  providedIn: 'root',
})
export class DocumentTypeService {
  constructor(private apiService: ApiService) {}

  //loclahost/api/documenttypes/fetchalldocumenttypes
  GetDocumentTypesAsync(): Observable<DocumentType[]> {
    return this.apiService.send<DocumentType[]>(
      'GET',
      environment.UrlConstants.DocumentType.GetAllDocumentTypes,
    );
  }

  //locahost/api/documenttypes/fetchdocumenttype/1
  GetDocumentTypeAsync(documentTypeId: number): Observable<DocumentType> {
    return this.apiService.send<DocumentType>(
      'GET',
      `${environment.UrlConstants.DocumentType.GetDocumentType}/${documentTypeId}`,
    );
  }

  InsertOrUpdateDocumentTypeAsync(documentType: DocumentType): Observable<any> {
    return this.apiService.send<any>(
      'POST',
      environment.UrlConstants.DocumentType.InsertOrUpdateDocumentType,
      documentType,
    );
  }

  DeleteDocumentTypeAsync(documentTypeId: number): Observable<any> {
    return this.apiService.send<DocumentType>(
      'DELETE',
      `${environment.UrlConstants.DocumentType.DeleteDocumentType}/${documentTypeId}`,
    );
  }
}
