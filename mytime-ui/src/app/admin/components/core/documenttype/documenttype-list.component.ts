import { Component, OnInit } from '@angular/core';
import { DocumentTypeService } from '../../../services/document_type.service';
import { LoaderService } from '../../../../common/services/loader.service';
import { AuditFieldsService } from '../../../../common/services/auditfields.service';
import { ToastrService } from 'ngx-toastr';
import { DocumentType } from '../../../models/document_type';

@Component({
  selector: 'app-documenttype-list',
  standalone: true,
  imports: [],
  templateUrl: './documenttype-list.component.html',
  styleUrl: './documenttype-list.component.css'
})
export class DocumenttypeListComponent implements OnInit {
  documentTypes: DocumentType[] = [];

  constructor(private documentTypeService: DocumentTypeService,
    private loader: LoaderService,
    private audit: AuditFieldsService,
    private toster: ToastrService
  ) {

  }

  ngOnInit(): void {
    this.loadIntialData();
  }

  loadIntialData(): void {
    this.loader.show();
    this.documentTypeService.GetDocumentTypesAsync().subscribe(response => {
      this.documentTypes = response;
      this.loader.hide();
    });
  }
}
