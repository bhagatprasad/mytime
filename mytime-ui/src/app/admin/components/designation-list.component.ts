import { Component, HostListener, OnInit } from '@angular/core';
import { DesignationService } from '../services/designation.service';
import { AllCommunityModule, ColDef, GridApi, GridOptions, GridReadyEvent, ICellRendererParams, ModuleRegistry, ValueFormatterParams } from 'ag-grid-community';
import { Designation } from '../models/designation';
import { CommonEngine } from '@angular/ssr';
import { CommonModule, DatePipe } from '@angular/common';
import { ToastrService } from 'ngx-toastr';
import { AgGridAngular } from 'ag-grid-angular';
import { FormsModule } from '@angular/forms';
import { CreateRoleComponent } from './create-role.component';
import { MobileActionsRendererComponent } from '../../common/components/mobile-actions-renderer.component';
import { ActionsRendererComponent } from '../../common/components/actions-renderer.component';
import { LoaderService } from '../../common/services/loader.service';
import { AuditFieldsService } from '../../common/services/auditfields.service';
import { CreateDesignationComponent } from './create-designation.component';

ModuleRegistry.registerModules([AllCommunityModule]);

@Component({
  selector: 'app-designation-list',
  standalone: true,
  imports: [CommonModule, AgGridAngular, DatePipe, FormsModule, CreateDesignationComponent],
  templateUrl: './designation-list.component.html',
  styleUrl: './designation-list.component.css'
})
export class DesignationListComponent implements OnInit {

  today = new Date();
  // Grid API
  private gridApi!: GridApi;

  // Responsive state
  isMobile: boolean = false;

  // Desktop Columns (7-8 columns)
  desktopColumnDefs: ColDef[] = [
    {
      field: 'DesignationId',
      headerName: 'ID',
      width: 80,
      filter: 'agNumberColumnFilter',
      sortable: true,
      cellClass: 'text-center'
    },
    {
      field: 'Name',
      headerName: 'Name',
      width: 120,
      filter: 'agTextColumnFilter',
      sortable: true,
      cellRenderer: this.nameRenderer.bind(this)
    },
    {
      field: 'Code',
      headerName: 'Code',
      width: 120,
      filter: 'agTextColumnFilter',
      sortable: true,
      cellClass: 'text-center'
    },
    {
      field: 'IsActive',
      headerName: 'Status',
      width: 120,
      filter: 'agTextColumnFilter',
      sortable: true,
      cellRenderer: this.statusRenderer.bind(this),
      cellClass: this.statusCellClass.bind(this)
    },
    {
      field: 'CreatedBy',
      headerName: 'Created By',
      width: 120,
      filter: 'agNumberColumnFilter',
      sortable: true,
      cellClass: 'text-center'
    },
    {
      field: 'CreatedOn',
      headerName: 'Created Date',
      width: 120,
      filter: 'agDateColumnFilter',
      sortable: true,
      valueFormatter: this.dateFormatter.bind(this),
      cellClass: 'text-center'
    },
    {
      field: 'ModifiedBy',
      headerName: 'Modified By',
      width: 120,
      filter: 'agNumberColumnFilter',
      sortable: true,
      cellClass: 'text-center'
    },
    {
      field: 'ModifiedOn',
      headerName: 'Last Modified',
      width: 120,
      filter: 'agDateColumnFilter',
      sortable: true,
      valueFormatter: this.dateFormatter.bind(this),
      cellClass: 'text-center'
    },
    {
      field: 'Actions',
      headerName: 'Actions',
      width: 150,
      sortable: false,
      filter: false,
      cellRenderer: ActionsRendererComponent,
      cellRendererParams: {
        onEditClick: (data: any) => this.requestadesignationProcess(data),
        onDeleteClick: (data: any) => this.deleteDesignation(data)
      },
      cellClass: 'text-center'
    }
  ];

  mobileColumnDefs: ColDef[] = [
    {
      field: 'Name',
      headerName: 'Designation',
      width: 180,
      cellRenderer: this.mobileNameRenderer.bind(this)
    },
    {
      field: 'Code',
      headerName: 'Code',
      width: 100,
      cellClass: 'text-center'
    },
    {
      field: 'Actions',
      headerName: '',
      width: 80,
      sortable: false,
      filter: false,
      cellRenderer: MobileActionsRendererComponent,
      cellRendererParams: {
        onEditClick: (data: any) => this.requestadesignationProcess(data)
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

  gridOptions: GridOptions = {
    pagination: true,
    paginationPageSize: 10,
    paginationPageSizeSelector: [10, 20, 50, 100],
    rowSelection: 'single',
    animateRows: true,
    enableCellTextSelection: true,
    suppressRowClickSelection: false,
    domLayout: 'autoHeight'
  };

  rowData: Designation[] = [];

  isLoading: boolean = false;

  showSidebar: boolean = false;
  selectedDes: Designation | null = null;

  constructor(
    private designationService: DesignationService,
    private toastr: ToastrService,
    private loader: LoaderService,
    private audit: AuditFieldsService
  ) { }

  ngOnInit(): void {
    this.checkScreenSize();
    this.setupResponsiveColumns();
    this.loadRoleData();
    window.addEventListener('resize', this.onResize.bind(this));
  }

  ngOnDestroy(): void {
    window.removeEventListener('resize', this.onResize.bind(this));
  }

  @HostListener('window:resize', ['$event'])
  onResize(event: any): void {
    this.checkScreenSize();
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

  loadRoleData(): void {
    this.loader.show();

    this.designationService.getDesignationsListAsync().subscribe({
      next: (des: Designation[]) => {
        this.rowData = des;
        this.loader.hide();
        if (this.gridApi) {
          setTimeout(() => {
            this.gridApi.sizeColumnsToFit();
          }, 100);
        }
      },
      error: (error) => {
        console.error('Error loading designations:', error);
        this.loader.hide();

        this.toastr.error('Failed to load designations.', 'Error');
      }
    });
  }

  onGridReady(params: GridReadyEvent): void {
    this.gridApi = params.api;
    setTimeout(() => {
      this.gridApi.sizeColumnsToFit();
    }, 300);
  }

  nameRenderer(params: ICellRendererParams): string {
    return `
        <div class="role-name-cell">
          <strong>${params.value}</strong>
          <div class="text-muted small">Code: ${params.data.Code}</div>
        </div>
      `;
  }

  mobileNameRenderer(params: ICellRendererParams): string {
    return `
        <div class="mobile-role-cell">
          <strong>${params.value}</strong>
          <div class="text-muted small">ID: ${params.data.Id}</div>
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

  mobileStatusRenderer(params: ICellRendererParams): string {
    const isActive = params.value;
    const statusText = isActive ? 'Active' : 'Inactive';
    const statusClass = isActive ? 'success' : 'danger';

    return `<span class="badge bg-${statusClass}">${statusText}</span>`;
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
      day: 'numeric'
    });
  }

  refreshData(): void {
    this.loadRoleData();
  }

  addNewRole(): void {
    this.toastr.info('Add new role functionality will be implemented', 'Coming Soon');
    console.log('Add new role clicked');
  }


  getSelectedRowsCount(): number {
    return this.gridApi?.getSelectedRows()?.length || 0;
  }

  getTotalRowsCount(): number {
    return this.rowData.length;
  }

  getActiveRolesCount(): number {
    return this.rowData.filter(des => des.IsActive).length;
  }

  getInactiveRolesCount(): number {
    return this.rowData.filter(des => !des.IsActive).length;
  }
  deleteDesignation(des: Designation): void {
    console.log(JSON.stringify(des));
  }

  requestadesignationProcess(des: Designation): void {
    this.selectedDes = des;
    this.showSidebar = true;
  }
  openAddEditDesignation(): void {
    this.selectedDes = null;
    this.showSidebar = true;
  }

  onSaveDesignation(des: Designation): void {
    this.loader.show();
    const _des = this.audit.appendAuditFields(des);

    console.log("Received designation:", _des);

    this.designationService.insertOrUpdateDesignation(_des).subscribe(
      response => {
        this.loader.hide();   // ✅ add this

        if (response) {
          this.toastr.success("Designation processed successfully");
          this.showSidebar = false;
          this.refreshData();
        }
      },
      error => {
        this.loader.hide();   // already here
        console.error(error);
        this.toastr.error("Something went wrong, please check and resubmit");
        this.showSidebar = true;
      }
    );
  }
  onCloseSidebar(): void {
    this.showSidebar = false;
  }

  showDeletePopup = false;

  deleteId: number | null = null;

  openDeletePopup(id: number) {
    this.deleteId = id;
    this.showDeletePopup = true;
  }
  closePopup() {
    this.showDeletePopup = false;
    this.deleteId = null;
  }
  confirmDelete() {
    if (!this.deleteId) return;

    this.designationService.deleteDesignationAsync(this.deleteId)
      .subscribe(() => {
        this.refreshData(); // refresh list
        this.showDeletePopup = false;
      });
  }
}


