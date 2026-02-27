import { Component, HostListener, OnInit } from '@angular/core';
import { DocumentTypeService } from '../../../services/document_type.service';
import { LoaderService } from '../../../../common/services/loader.service';
import { AuditFieldsService } from '../../../../common/services/auditfields.service';
import { ToastrService } from 'ngx-toastr';
import { DocumentType } from '../../../models/document_type';
import {
  AllCommunityModule,
  ColDef,
  GridApi,
  GridOptions,
  GridReadyEvent,
  ICellRendererParams,
  ModuleRegistry,
  ValueFormatterParams,
} from 'ag-grid-community';
import { response } from 'express';
import { MobileActionsRendererComponent } from '../../../../common/components/mobile-actions-renderer.component';
import { CommonModule } from '@angular/common';
import { AgGridAngular } from 'ag-grid-angular';

// Register AG Grid modules
ModuleRegistry.registerModules([AllCommunityModule]);

@Component({
  selector: 'app-documenttype-list',
  standalone: true,
  imports: [CommonModule, AgGridAngular],
  templateUrl: './documenttype-list.component.html',
  styleUrl: './documenttype-list.component.css',
})
export class DocumenttypeListComponent implements OnInit {
  requestRoleProcess(data: any) {
    throw new Error('Method not implemented.');
  }
  today = new Date();
  private gridApi!: GridApi;
  columnDefs: ColDef[] = [];

  defaultColDef: ColDef = {
    flex: 1,
    minWidth: 100,
    filter: true,
    resizable: true,
    sortable: true,
    floatingFilter: false,
  };

  gridOptions: GridOptions = {
    pagination: true,
    paginationPageSize: 10,
    paginationPageSizeSelector: [20, 40, 80, 100],
    rowSelection: 'single',
    animateRows: true,
    enableCellTextSelection: true,
    suppressRowClickSelection: false,
    domLayout: 'autoHeight',
  };

  desktopColumnDefs: ColDef[] = [
    {
      field: 'Id',
      headerName: 'ID',
      width: 80,
      filter: 'agNumberColumnFilter',
      sortable: true,
      cellClass: 'text-left',
    },
    {
      field: 'Name',
      headerName: 'Name',
      width: 130,
      filter: 'agTextColumnFilter',
      sortable: true,
      cellRenderer: this.nameRenderer.bind(this),
    },

    {
      field: 'CreatedBy',
      headerName: 'Created By',
      width: 80,
      filter: 'agNumberColumnFilter',
      sortable: true,
      cellClass: 'text-left',
    },
    {
      field: 'CreatedOn',
      headerName: 'Created Date',
      width: 120,
      filter: 'agDateColumnFilter',
      sortable: true,
      valueFormatter: this.dateFormatter.bind(this),
      cellClass: 'text-left',
    },
    {
      field: 'ModifiedBy',
      headerName: 'Modified By',
      width: 80,
      filter: 'agNumberColumnFilter',
      sortable: true,
      cellClass: 'text-left',
    },
    {
      field: 'ModifiedOn',
      headerName: 'Last Modified',
      width: 120,
      filter: 'agDateColumnFilter',
      sortable: true,
      valueFormatter: this.dateFormatter.bind(this),
      cellClass: 'text-left',
    },
    {
      field: 'IsActive',
      headerName: 'Status',
      width: 120,
      filter: 'agTextColumnFilter',
      sortable: true,
      cellRenderer: this.statusRenderer.bind(this),
      cellClass: this.statusCellClass.bind(this),
    },
  ];

  mobileColumnDefs: ColDef[] = [
    {
      field: 'Id',
      headerName: 'ID',
      width: 40,
      cellClass: 'text-left',
    },
    {
      field: 'Name',
      headerName: 'Name',
      width: 80,
      cellRenderer: this.nameRenderer.bind(this),
    },
  ];

  documentTypes: DocumentType[] = [];

  isMobile: boolean = false;

  constructor(
    private documentTypeService: DocumentTypeService,
    private loader: LoaderService,
    private audit: AuditFieldsService,
    private toaster: ToastrService,
  ) {}

  ngOnInit(): void {
    this.checkScreenSize();
    this.setupResponsiveColumns();
    this.loadIntialData();
    window.addEventListener('resize', this.onResize.bind(this));
  }

  loadIntialData(): void {
    this.loader.show();

    this.documentTypeService.GetDocumentTypesAsync().subscribe({
      next: (documenttype: DocumentType[]) => {
        console.log('Document Types', documenttype);

        this.documentTypes = documenttype;
        this.loader.hide();

        if (this.gridApi) {
          setTimeout(() => {
            this.gridApi.sizeColumnsToFit();
          }, 100);
        }
      },
      error: (error) => {
        console.error('Error loading documenttype:', error);
        this.toaster.error('Failed to load documenttype', 'Error');
        this.loader.hide();
      },
    });
  }

  onGridReady(params: GridReadyEvent): void {
    this.gridApi = params.api;
    setTimeout(() => {
      this.gridApi.sizeColumnsToFit();
    }, 300);
  }

  ngOnDestroy(): void {
    window.removeEventListener('resize', this.onResize.bind(this));
  }

  @HostListener('window:resize', ['$event'])
  onResize(event: any): void {
    this.checkScreenSize();
  }

  getTotalRowsCount(): number {
    return this.documentTypes.length;
  }

  openAddEditDocumentType(): void {}

  nameRenderer(params: ICellRendererParams): string {
    return `
        <div class="role-name-cell">
          <strong>${params.value}</strong>
          <div class="text-muted small">Code: ${params.data.Code}</div>
        </div>
      `;
  }
  statusRenderer(params: ICellRendererParams): string {
    const isActive = params.value;
    const statusText = isActive ? 'Active' : 'Inactive';
    const statusClass = isActive ? 'success' : 'danger';
    const icon = isActive ? 'mdi-check-circle' : 'mdi-close-circle';

    return `
      <div class="d-flex align-items-center gap-2">
        <i class="mdi ${icon} text-${statusClass}"></i>
        <span class="badge bg-${statusClass}">${statusText}</span>
      </div>
    `;
  }
  statusCellClass(params: any): string {
    const isActive = params.value;
    return isActive ? 'status-active' : 'status-inactive';
  }
  dateFormatter(params: ValueFormatterParams): string {
    if (!params.value) return 'N/A';

    const date = new Date(params.value);
    if (isNaN(date.getTime())) return 'Invalid Date';

    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
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
      this.gridOptions.domLayout = 'autoHeight';
    } else {
      this.columnDefs = [...this.desktopColumnDefs];
      this.gridOptions.domLayout = 'normal';
    }
    if (this.gridApi) {
      this.refreshGridColumns();
    }
  }

  private refreshGridColumns(): void {
    if (!this.gridApi) return;
    const newColumnDefs = JSON.parse(JSON.stringify(this.columnDefs));
    setTimeout(() => {
      this.gridApi.refreshHeader();
      this.gridApi.sizeColumnsToFit();
    }, 100);
  }
  // refreshGridColumns() {
  //   throw new Error('Method not implemented.');
  // }
}
