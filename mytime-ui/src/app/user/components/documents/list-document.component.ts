import { CommonModule } from '@angular/common';
import { Component, HostListener, OnDestroy, OnInit } from '@angular/core';
import { AllCommunityModule, ColDef, GridApi, GridOptions, GridReadyEvent, ModuleRegistry } from 'ag-grid-community';
import { EmployeeDocument } from '../../../admin/models/employee_document';
import { MobileActionsDocumentRendererComponent } from '../../../common/components/mobile-actions-document.renderer.component';
import { ActionsDocumentRendererComponent } from '../../../common/components/actions-document.renderer.component';
import { DocumentService } from '../../../admin/services/document.service';
import { LoaderService } from '../../../common/services/loader.service';
import { ToastrService } from 'ngx-toastr';
import { AuditFieldsService } from '../../../common/services/auditfields.service';
import { StorageService } from '../../../common/services/storage.service';
import { forkJoin } from 'rxjs';
import { AccountService } from '../../../common/services/account.service';
import { ApplicationUser } from '../../../common/models/application-user';
import { EmployeeService } from '../../../admin/services/employee.service';
import { Employee } from '../../../admin/models/employee';
import { AgGridAngular } from 'ag-grid-angular';

ModuleRegistry.registerModules([AllCommunityModule]);

@Component({
  selector: 'app-list-document',
  standalone: true,
  imports: [CommonModule, AgGridAngular],
  templateUrl: './list-document.component.html',
  styleUrl: './list-document.component.css'
})
export class ListDocumentComponent implements OnInit, OnDestroy {
  applicationUser: ApplicationUser | null = null;
  employee: Employee | null = null;
  private documentsGridApi!: GridApi;
  isMobile: boolean = false;
  documents: EmployeeDocument[] = [];
  showDocumentForm = false;
  selectedDocument: EmployeeDocument | null = null;

  desktopColumnDefs: ColDef[] = [
    {
      field: 'FileName',
      headerName: 'File Name',
      width: 180,
      filter: 'agTextColumnFilter',
      sortable: true
    },
    {
      field: 'DocumentType',
      headerName: 'Document Type',
      width: 150,
      filter: 'agTextColumnFilter',
      sortable: true
    },
    {
      field: 'ContentType',
      headerName: 'Content Type',
      width: 150,
      filter: 'agTextColumnFilter',
      sortable: true
    },
    {
      field: 'UploadTimestamp',
      headerName: 'Uploaded On',
      width: 170,
      sortable: true,
      valueFormatter: (params) =>
        params.value ? new Date(params.value).toLocaleString() : ''
    },
    {
      headerName: 'Actions',
      width: 180,
      sortable: false,
      filter: false,
      cellRenderer: ActionsDocumentRendererComponent,
      cellRendererParams: {
        onDownloadClick: (data: any) => this.downloadDocument(data),
        onDeleteClick: (data: any) => this.deleteDocument(data)
      },
      cellClass: 'text-center'
    }
  ];

  mobileColumnDefs: ColDef[] = [
    {
      field: 'employeeInfo',
      headerName: 'Employee & Document',
      width: 200,
      cellRenderer: (params: any) => {
        const document = params.data as EmployeeDocument;
        return `<div class="employee-document-info">
            <div class="document-name">${document.FileName || 'No file name'}</div>
            <div class="document-type text-muted">${document.DocumentType || 'No type'}</div>
          </div>`;
      },
      cellClass: 'employee-document-cell'
    },
    {
      headerName: 'Actions',
      width: 110,
      sortable: false,
      filter: false,
      cellRenderer: MobileActionsDocumentRendererComponent,
      cellRendererParams: {
        onDownloadClick: (data: any) => this.downloadDocument(data),
        onDeleteClick: (data: any) => this.deleteDocument(data)
      },
      cellClass: 'text-center'
    }
  ];

  columnDefs: ColDef[] = [];

  defaultColDef: ColDef = {
    flex: 1,
    minWidth: 100,
    filter: true,
    resizable: true,
    sortable: true,
    floatingFilter: false
  };

  documentsGridOptions: GridOptions = {
    pagination: true,
    paginationPageSize: 10,
    paginationPageSizeSelector: [10, 20, 50, 100],
    rowSelection: 'single',
    animateRows: true,
    enableCellTextSelection: true,
    suppressRowClickSelection: false,
    domLayout: 'autoHeight'
  };

  constructor(
    private documentService: DocumentService,
    private loader: LoaderService,
    private notify: ToastrService,
    private audit: AuditFieldsService,
    private storageService: StorageService,
    private accountService: AccountService,
    private employeeService: EmployeeService
  ) { }

  ngOnDestroy(): void {
    window.removeEventListener('resize', this.onResize.bind(this));
  }

  ngOnInit(): void {
    this.applicationUser = this.accountService.getCurrentUser();
    if (this.applicationUser?.id) {
      this.loadEmployeeData();
    } else {
      this.loader.show();
      this.notify.error('User not authenticated', 'Error');
      this.loader.hide();
    }

    this.checkScreenSize();
    this.setupResponsiveColumns();
    window.addEventListener('resize', this.onResize.bind(this));
  }

  loadEmployeeData(): void {
    this.loader.show();
    this.employeeService.GetEmployeeByUserIdAsync(this.applicationUser?.id).subscribe({
      next: (response) => {
        this.employee = response;
        this.loadDocumentsData();
      },
      error: (error) => {
        console.error('Error loading employee data:', error);
        this.loader.hide();
        this.notify.error('Failed to load employee information', 'Error');
      }
    });
  }

  loadDocumentsData(): void {
    if (!this.employee?.EmployeeId) {
      this.loader.hide();
      this.notify.warning('Employee ID not found', 'Warning');
      return;
    }

    this.loader.show();
    forkJoin({
      documents: this.documentService.getDocumentsByEmployeeAsync(this.employee.EmployeeId)
    }).subscribe({
      next: (result: { documents: EmployeeDocument[] }) => {
        this.documents = result.documents;

        if (this.documentsGridApi) {
          setTimeout(() => {
            this.documentsGridApi.sizeColumnsToFit();
          }, 100);
        }
        this.loader.hide();
      },
      error: (error) => {
        console.error('Error loading documents:', error);
        this.loader.hide();
        this.notify.error('Failed to load employee documents', 'Error');
      }
    });
  }

  private checkScreenSize(): void {
    const wasMobile = this.isMobile;
    this.isMobile = window.innerWidth < 768;

    if (wasMobile !== this.isMobile) {
      this.setupResponsiveColumns();

      if (this.documentsGridApi) {
        setTimeout(() => {
          this.documentsGridApi.refreshHeader();
          this.documentsGridApi.sizeColumnsToFit();
        }, 100);
      }
    }
  }

  private setupResponsiveColumns(): void {
    if (this.isMobile) {
      this.columnDefs = [...this.mobileColumnDefs];
      this.documentsGridOptions.domLayout = 'autoHeight';
    } else {
      this.columnDefs = [...this.desktopColumnDefs];
      this.documentsGridOptions.domLayout = 'normal';
    }

    if (this.documentsGridApi) {
      this.refreshGridColumns();
    }
  }

  private refreshGridColumns(): void {
    if (!this.documentsGridApi) return;
    setTimeout(() => {
      this.documentsGridApi.refreshHeader();
      this.documentsGridApi.sizeColumnsToFit();
    }, 100);
  }

  onGridReady(params: GridReadyEvent): void {
    this.documentsGridApi = params.api;
    setTimeout(() => {
      this.documentsGridApi.sizeColumnsToFit();
    }, 300);
  }

  @HostListener('window:resize')
  onResize(): void {
    this.checkScreenSize();
  }

  refreshData(): void {
    this.loadDocumentsData();
  }

  getTotalRowsCount(): number {
    return this.documents.length;
  }

  getActiveDocumentsCount(): number {
    return this.documents.filter(x => x.IsActive === true).length;
  }

  deleteDocument(eDocument: EmployeeDocument): void {
    if (!eDocument.FileId) {
      this.notify.error('File information is missing');
      return;
    }

    this.loader.show();

    this.storageService.deleteFile(eDocument.FileId)
      .then(() => {
        return this.documentService.removeEmployeeDocumentAsync(eDocument.EmployeeDocumentId).toPromise();
      })
      .then(() => {
        this.notify.success('Document deleted successfully');
        this.loadDocumentsData();
      })
      .catch((error) => {
        console.error('Error deleting document:', error);
        this.notify.error('Failed to delete the document');
      })
      .finally(() => {
        this.loader.hide();
      });
  }

  downloadDocument(eDocument: EmployeeDocument): void {
    try {
      if (!eDocument.FileInfo || !eDocument.FileId || !eDocument.FileName) {
        this.notify.error('File information is missing');
        return;
      }

      const fileInfo = JSON.parse(eDocument.FileInfo);
      const uploadTime = new Date(eDocument.UploadTimestamp ?? 0).getTime();
      const isExpired = (Date.now() - uploadTime) > 3600 * 1000;

      if (isExpired) {
        this.loader.show();
        this.storageService.getDownloadUrl(eDocument.FileId, 3600, eDocument.FileName)
          .then(result => {
            this.triggerDownload(result.url, eDocument.FileName!);
            this.loader.hide();
          })
          .catch(error => {
            console.error('Error getting download URL:', error);
            this.notify.error('Failed to generate download link');
            this.loader.hide();
          });
      } else {
        this.triggerDownload(fileInfo.downloadUrl, eDocument.FileName);
      }

    } catch (error) {
      console.error('Error parsing FileInfo:', error);
      this.notify.error('Failed to download the file');
    }
  }

  private triggerDownload(url: string, filename: string): void {
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    link.target = '_blank';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }

  onFirstDataRendered(params: any): void {
    setTimeout(() => {
      if (this.documentsGridApi) {
        this.documentsGridApi.sizeColumnsToFit();
      }
    }, 100);
  }
  uploadDocument(): void {
  }
}