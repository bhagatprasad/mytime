import { CommonModule } from '@angular/common';
import { Component, HostListener, Input, OnDestroy, OnInit } from '@angular/core';
import { AgGridAngular } from 'ag-grid-angular';
import { AllCommunityModule, ColDef, GridApi, GridOptions, GridReadyEvent, ModuleRegistry } from 'ag-grid-community';
import { EmployeeDocument } from '../../../models/employee_document';
import { ActionsRendererComponent } from '../../../../common/components/actions-renderer.component';
import { MobileActionsRendererComponent } from '../../../../common/components/mobile-actions-renderer.component';
import { DocumentService } from '../../../services/document.service';
import { LoaderService } from '../../../../common/services/loader.service';
import { ToastrService } from 'ngx-toastr';
import { AuditFieldsService } from '../../../../common/services/auditfields.service';
import { UploadDocumentComponent } from './upload.component';


ModuleRegistry.registerModules([AllCommunityModule]);

@Component({
  selector: 'app-document-list',
  standalone: true,
  imports: [CommonModule, AgGridAngular, UploadDocumentComponent],
  templateUrl: './list.component.html',
  styleUrl: './list.component.css'
})
export class ListDocumentsComponent implements OnInit, OnDestroy {

  @Input() employeeId: number = 0;

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
      cellRenderer: ActionsRendererComponent,
      cellRendererParams: {
        onDownloadClick: (data: any) => this.downloadDocument(data),
        onDeleteClick: (data: any) => this.deleteDocument(data)
      },
      cellClass: 'text-center'
    }
  ];


  mobileColumnDefs: ColDef[] = [
    {
      field: 'FileName',
      headerName: 'Document',
      width: 160
    },
    {
      field: 'Document Type',
      headerName: 'DocumentType',
      width: 140,
      valueFormatter: (params) =>
        params.value ? new Date(params.value).toLocaleDateString() : ''
    },
    {
      headerName: '',
      width: 110,
      sortable: false,
      filter: false,
      cellRenderer: MobileActionsRendererComponent,
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
    private audit: AuditFieldsService) { }
  ngOnDestroy(): void {
    window.removeEventListener('resize', this.onResize.bind(this));
  }
  ngOnInit(): void {
    this.checkScreenSize();
    this.setupResponsiveColumns();
    this.loadDocumnetsData();
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

  loadDocumnetsData(): void {
    if (!this.employeeId) return;

    this.loader.show();
    this.documentService.getDocumentsByEmployeeAsync(this.employeeId).subscribe({
      next: (employeeDocument: EmployeeDocument[]) => {
        this.documents = employeeDocument;
        this.loader.hide();
        if (this.documentsGridApi) {
          setTimeout(() => {
            this.documentsGridApi.sizeColumnsToFit();
          }, 100);
        }
      },
      error: (error) => {
        console.error('Error loading employee documents:', error);
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
    this.loadDocumnetsData();
  }

  onSaveEmployeeDocument(employeeDocument: EmployeeDocument): void {
    console.log(employeeDocument);
    this.loader.show();
    if (!employeeDocument.EmployeeDocumentId && this.employeeId) {
      employeeDocument.EmployeeId = this.employeeId;
    }

    const _contact = this.audit.appendAuditFields(employeeDocument);
    this.documentService.insertOrUpdateEmployeeDocumentAsync(_contact).subscribe({
      next: (response) => {
        if (response) {
          this.notify.success('Education saved successfully');
          this.showDocumentForm = false;
          this.selectedDocument = null;
          this.loadDocumnetsData();
        }
      },
      error: (error) => {
        console.error('Error saving education:', error);
        this.notify.error('Failed to save education');
        this.loader.hide();
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

  getTotalRowsCount(): number {
    return this.documents.length;
  }

  getActiveDocumentsCount(): number {
    return this.documents.filter(x => x.IsActive == true).length;
  }

  deleteDocument(eDocument: EmployeeDocument): void {

  }
  downloadDocument(eDocument: EmployeeDocument): void {

  }
}
