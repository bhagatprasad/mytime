import { CommonModule } from '@angular/common';
import { Component, HostListener, Input, OnDestroy, OnInit } from '@angular/core';
import { AgGridAngular } from 'ag-grid-angular';
import { AllCommunityModule, ColDef, GridApi, GridOptions, GridReadyEvent, ModuleRegistry } from 'ag-grid-community';
import { UploadDocumentComponent } from './upload-document.component';
import { EmployeeDocument } from '../../../admin/models/employee_document';
import { ActionsDocumentRendererComponent } from '../../../common/components/actions-document.renderer.component';
import { MobileActionsDocumentRendererComponent } from '../../../common/components/mobile-actions-document.renderer.component';
import { DocumentService } from '../../../admin/services/document.service';
import { LoaderService } from '../../../common/services/loader.service';
import { ToastrService } from 'ngx-toastr';
import { AuditFieldsService } from '../../../common/services/auditfields.service';
import { StorageService } from '../../../common/services/storage.service';
import { AccountService } from '../../../common/services/account.service';

ModuleRegistry.registerModules([AllCommunityModule]);

@Component({
  selector: 'app-document-list',
  standalone: true,
  imports: [CommonModule, AgGridAngular, UploadDocumentComponent],
  templateUrl: './list-document.component.html',
  styleUrl: './list-document.component.css'
})
export class ListDocumentComponent implements OnInit, OnDestroy {

  employeeId: any = 0;

  private documentsGridApi!: GridApi;

  isMobile: boolean = false;
  documents: EmployeeDocument[] = [];

  showDocumentForm = false;
  selectedDocument: EmployeeDocument | null = null;

  // ✅ Desktop Columns
  desktopColumnDefs: ColDef[] = [
    { field: 'FileName', headerName: 'File Name', width: 180 },
    { field: 'DocumentType', headerName: 'Document Type', width: 150 },
    { field: 'ContentType', headerName: 'Content Type', width: 150 },
    {
      field: 'UploadTimestamp',
      headerName: 'Uploaded On',
      width: 170,
      valueFormatter: (params) =>
        params.value ? new Date(params.value).toLocaleString() : ''
    },
    {
      headerName: 'Actions',
      width: 180,
      cellRenderer: ActionsDocumentRendererComponent,
      cellRendererParams: {
        onDownloadClick: (data: any) => this.downloadDocument(data),
        onDeleteClick: (data: any) => this.deleteDocument(data)
      }
    }
  ];

  // ✅ Mobile Columns
  mobileColumnDefs: ColDef[] = [
    { field: 'FileName', headerName: 'Document', width: 160 },
    { field: 'DocumentType', headerName: 'Type', width: 140 },
    {
      headerName: '',
      width: 110,
      cellRenderer: MobileActionsDocumentRendererComponent,
      cellRendererParams: {
        onDownloadClick: (data: any) => this.downloadDocument(data),
        onDeleteClick: (data: any) => this.deleteDocument(data)
      }
    }
  ];

  columnDefs: ColDef[] = [];

  defaultColDef: ColDef = {
    flex: 1,
    minWidth: 100,
    resizable: true,
    sortable: true
  };

  documentsGridOptions: GridOptions = {
    pagination: true,
    paginationPageSize: 10,
    rowSelection: 'single',
    animateRows: true,
    domLayout: 'autoHeight'
  };

  constructor(
    private accountService: AccountService,
    private documentService: DocumentService,
    private loader: LoaderService,
    private notify: ToastrService,
    private audit: AuditFieldsService,
    private storageService: StorageService
  ) { }

  // ================= Lifecycle =================

  ngOnInit(): void {
    this.checkScreenSize();
    this.setupResponsiveColumns();
    this.loadDocumentsData();
  }

  ngOnDestroy(): void {
    window.removeEventListener('resize', this.onResize);
  }

  // ================= Responsive =================

  @HostListener('window:resize')
  onResize(): void {
    this.checkScreenSize();
  }

  private checkScreenSize(): void {
    const prev = this.isMobile;
    this.isMobile = window.innerWidth < 768;

    if (prev !== this.isMobile) {
      this.setupResponsiveColumns();
    }
  }

  private setupResponsiveColumns(): void {
    this.columnDefs = this.isMobile
      ? [...this.mobileColumnDefs]
      : [...this.desktopColumnDefs];

    if (this.documentsGridApi) {
      setTimeout(() => {
        this.documentsGridApi.refreshHeader();
        this.documentsGridApi.sizeColumnsToFit();
      });
    }
  }

  // ================= Grid =================

  onGridReady(params: GridReadyEvent): void {
    this.documentsGridApi = params.api;
    setTimeout(() => this.documentsGridApi.sizeColumnsToFit(), 300);
  }

  // ================= Data =================

  loadDocumentsData(): void {
    this.loader.show();

    const user = this.accountService.getCurrentUser();
    
    if (!user?.employeeId) {
      console.warn('No logged-in user found');
      this.loader.hide();
      return;
    }

    this.employeeId = user?.employeeId;

    this.documentService.getDocumentsByEmployeeAsync(this.employeeId).subscribe({
      next: (res) => {
        this.documents = res || [];
        this.loader.hide();

        if (this.documentsGridApi) {
          setTimeout(() => this.documentsGridApi.sizeColumnsToFit(), 100);
        }
      },
      error: () => {
        this.loader.hide();
        this.notify.error('Failed to load documents');
      }
    });
  }

  refreshData(): void {
    this.loadDocumentsData();
  }

  // ================= CRUD =================

  onSaveEmployeeDocument(doc: EmployeeDocument): void {
    this.loader.show();

    if (!doc.EmployeeDocumentId) {
      doc.EmployeeId = this.employeeId;
    }

    const payload = this.audit.appendAuditFields(doc);

    this.documentService.insertOrUpdateEmployeeDocumentAsync(payload).subscribe({
      next: () => {
        this.notify.success('Document saved');
        this.showDocumentForm = false;
        this.selectedDocument = null;
        this.loadDocumentsData();
      },
      error: () => {
        this.loader.hide();
        this.notify.error('Save failed');
      }
    });
  }

  openAddEmployeeDocumentForm(): void {
    this.selectedDocument = null;
    this.showDocumentForm = true;
  }

  onCloseEmployeeDocumentForm(): void {
    this.selectedDocument = null;
    this.showDocumentForm = false;
  }

  // ================= Delete =================

  deleteDocument(doc: EmployeeDocument): void {
    if (!doc.FileId) {
      this.notify.error('File info missing');
      return;
    }

    this.loader.show();

    this.storageService.deleteFile(doc.FileId)
      .then(() => {
        this.documentService.removeEmployeeDocumentAsync(doc.EmployeeDocumentId).subscribe({
          next: () => {
            this.notify.success('Deleted');
            this.loadDocumentsData();
          },
          error: () => {
            this.notify.error('DB delete failed');
          }
        });
      })
      .catch(() => {
        this.notify.error('File delete failed');
      })
      .finally(() => this.loader.hide());
  }

  // ================= Download =================

  downloadDocument(doc: EmployeeDocument): void {
    try {
      if (!doc.FileInfo || !doc.FileId || !doc.FileName) {
        this.notify.error('File info missing');
        return;
      }

      const fileInfo = JSON.parse(doc.FileInfo);
      const uploadTime = new Date(doc.UploadTimestamp ?? 0).getTime();
      const expired = (Date.now() - uploadTime) > 3600 * 1000;

      if (expired) {
        this.storageService
          .getDownloadUrl(doc.FileId, 3600, doc.FileName)
          .then(res => this.triggerDownload(res.url, doc.FileName!));
      } else {
        this.triggerDownload(fileInfo.downloadUrl, doc.FileName);
      }

    } catch {
      this.notify.error('Download failed');
    }
  }

  private triggerDownload(url: string, filename: string): void {
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.target = '_blank';
    a.click();
    a.remove();
  }

  // ================= Stats =================

  getTotalRowsCount(): number {
    return this.documents.length;
  }

  getActiveDocumentsCount(): number {
    return this.documents.filter(x => x.IsActive).length;
  }
}