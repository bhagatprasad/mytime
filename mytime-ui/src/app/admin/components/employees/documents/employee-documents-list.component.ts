import { CommonModule } from '@angular/common';
import { Component, DestroyRef, HostListener, OnDestroy, OnInit } from '@angular/core';
import { AgGridAngular } from 'ag-grid-angular';
import { AllCommunityModule, ColDef, GridApi, GridOptions, GridReadyEvent, ModuleRegistry } from 'ag-grid-community';
import { DocumentService } from '../../../services/document.service';
import { LoaderService } from '../../../../common/services/loader.service';
import { EmployeeDocument } from '../../../models/employee_document';
import { ActionsDocumentRendererComponent } from '../../../../common/components/actions-document.renderer.component';
import { MobileActionsDocumentRendererComponent } from '../../../../common/components/mobile-actions-document.renderer.component';
import { ToastrService } from 'ngx-toastr';
import { AuditFieldsService } from '../../../../common/services/auditfields.service';
import { StorageService } from '../../../../common/services/storage.service';
import { EmployeeService } from '../../../services/employee.service';
import { forkJoin } from 'rxjs';
import { Employee } from '../../../models/employee';

ModuleRegistry.registerModules([AllCommunityModule]);

@Component({
  selector: 'app-employee-documents-list',
  standalone: true,
  imports: [CommonModule, AgGridAngular],
  templateUrl: './employee-documents-list.component.html',
  styleUrls: ['./employee-documents-list.component.css']
})
export class EmployeeDocumentsListComponent implements OnInit, OnDestroy {

  private documentsGridApi!: GridApi;

  isMobile: boolean = false;

  documents: EmployeeDocument[] = [];

  employees: Employee[] = [];

  showDocumentForm = false;

  selectedDocument: EmployeeDocument | null = null;

  private employeeMap: Map<number, Employee> = new Map();

  desktopColumnDefs: ColDef[] = [
    {
      field: 'employeeInfo',
      headerName: 'Employee',
      width: 200,
      filter: 'agTextColumnFilter',
      sortable: true,
      filterParams: {
        filterOptions: ['contains', 'notContains'],
        textFormatter: (r: any) => {
          if (r == null) return null;
          const document = r as EmployeeDocument;
          const employee = document.EmployeeId ? this.employeeMap.get(document.EmployeeId) : null;
          if (employee) {
            return `${employee.FirstName || ''} ${employee.LastName || ''} ${employee.EmployeeCode || ''}`.toLowerCase();
          }
          return 'unknown employee';
        }
      },
      valueGetter: (params) => {
        const document = params.data as EmployeeDocument;
        const employee = document.EmployeeId ? this.employeeMap.get(document.EmployeeId) : null;

        if (employee) {
          const employeeName = `${employee.FirstName || ''} ${employee.LastName || ''}`.trim();
          const employeeCode = employee.EmployeeCode ? ` (${employee.EmployeeCode})` : '';
          return `${employeeName}${employeeCode}`;
        }
        return 'Unknown Employee';
      },
      cellRenderer: (params: any) => {
        const document = params.data as EmployeeDocument;
        const employee = document.EmployeeId ? this.employeeMap.get(document.EmployeeId) : null;

        if (employee) {
          const employeeName = `${employee.FirstName || ''} ${employee.LastName || ''}`.trim() || 'Unknown Employee';
          const employeeCode = employee.EmployeeCode || '';
          const department = employee.DepartmentId ? 'Department ' + employee.DepartmentId : '';

          return `<div class="employee-info">
            <div class="employee-name"><strong>${employeeName}</strong></div>
            <div class="employee-details text-muted small">
              ${employeeCode ? `<span>Code: ${employeeCode}</span>` : ''}
              ${employeeCode && department ? ' • ' : ''}
              ${department ? `<span>${department}</span>` : ''}
            </div>
          </div>`;
        }

        return `<div class="employee-info">
          <div class="employee-name"><strong>Unknown Employee</strong></div>
          <div class="employee-details text-muted small">No employee assigned</div>
        </div>`;
      },
      cellClass: 'employee-desktop-cell'
    },
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
        const employee = document.EmployeeId ? this.employeeMap.get(document.EmployeeId) : null;

        if (employee) {
          const employeeName = `${employee.FirstName || ''} ${employee.LastName || ''}`.trim() || 'Unknown Employee';
          return `<div class="employee-document-info">
            <div class="employee-name"><strong>${employeeName}</strong></div>
            <div class="document-name">${document.FileName || 'No file name'}</div>
            <div class="document-type text-muted">${document.DocumentType || 'No type'}</div>
          </div>`;
        }

        return `<div class="employee-document-info">
          <div class="employee-name"><strong>Unknown Employee</strong></div>
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

  constructor(private documentService: DocumentService,
    private employeeService: EmployeeService,
    private loader: LoaderService,
    private notify: ToastrService,
    private audit: AuditFieldsService,
    private storageService: StorageService) {

  }

  ngOnDestroy(): void {
    window.removeEventListener('resize', this.onResize.bind(this));
  }

  ngOnInit(): void {
    this.checkScreenSize();
    this.setupResponsiveColumns();
    this.loadDocumentsData();
    window.addEventListener('resize', this.onResize.bind(this));
  }

  private checkScreenSize(): void {
    const wasMobile = this.isMobile;
    this.isMobile = window.innerWidth < 768;

    if (wasMobile !== this.isMobile) {
      this.setupResponsiveColumns();
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

  loadDocumentsData(): void {
    this.loader.show();

    forkJoin({
      employees: this.employeeService.getEmployeesListAsync(),
      documents: this.documentService.getEmployeeDocumentsAsync()
    }).subscribe({
      next: (result: { employees: Employee[], documents: EmployeeDocument[] }) => {
        this.employees = result.employees;
        this.employeeMap.clear();
        this.employees.forEach(employee => {
          if (employee.EmployeeId) {
            this.employeeMap.set(employee.EmployeeId, employee);
          }
        });

        this.documents = result.documents;

        this.loader.hide();

        if (this.documentsGridApi) {
          setTimeout(() => {
            this.documentsGridApi.sizeColumnsToFit();
          }, 100);
        }
      },
      error: (error) => {
        console.error('Error loading data:', error);
        this.loader.hide();
        this.notify.error('Failed to load employee documents', 'Error');
      }
    });
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
    return this.documents.filter(x => x.IsActive == true).length;
  }

  deleteDocument(eDocument: EmployeeDocument): void {
    if (!eDocument.FileId) {
      this.notify.error('File information is missing');
      return;
    }

    this.loader.show();

    this.storageService.deleteFile(eDocument.FileId)
      .then(() => {
        this.documentService.removeEmployeeDocumentAsync(eDocument.EmployeeDocumentId).subscribe({
          next: () => {
            this.notify.success('Document deleted successfully');
            this.loadDocumentsData();
          },
          error: (error) => {
            console.error('Error deleting from database:', error);
            this.notify.error('File deleted from cloud but failed to remove from database');
          }
        });
      })
      .catch((error) => {
        console.error('Error deleting file from cloud:', error);
        this.notify.error('Failed to delete the file');
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
        this.storageService.getDownloadUrl(eDocument.FileId, 3600, eDocument.FileName)
          .then(result => this.triggerDownload(result.url, eDocument.FileName!));
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
    link.click();
    link.remove();
  }

  onFirstDataRendered(params: any): void {
    setTimeout(() => {
      if (this.documentsGridApi) {
        this.documentsGridApi.sizeColumnsToFit();
      }
    }, 100);
  }
}