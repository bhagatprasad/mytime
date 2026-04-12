import { Component, HostListener, OnDestroy, OnInit } from '@angular/core';
import { DepartmentService } from '../../../services/department.service';
import { Department } from '../../../models/department';
import { CommonModule, DatePipe } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AllCommunityModule, ColDef, GridApi, GridOptions, GridReadyEvent, ICellRendererParams, ModuleRegistry, ValueFormatterParams } from 'ag-grid-community';
import { AgGridAngular } from 'ag-grid-angular';
import { LoaderService } from '../../../../common/services/loader.service';
import { ToastrService } from 'ngx-toastr';
import { AuditFieldsService } from '../../../../common/services/auditfields.service';
import { ActionsRendererComponent } from '../../../../common/components/actions-renderer.component';
import { MobileActionsRendererComponent } from '../../../../common/components/mobile-actions-renderer.component';
import { CreateDepartmentComponent } from './create-department.component';
ModuleRegistry.registerModules([AllCommunityModule]);

@Component({
  selector: 'app-department-list',
  standalone: true,
  imports: [CommonModule, FormsModule, AgGridAngular, DatePipe, CreateDepartmentComponent],
  templateUrl: './department-list.component.html',
  styleUrl: './department-list.component.css'
})
export class DepartmentListComponent implements OnInit, OnDestroy {

  private gridApi!: GridApi;

  today = new Date();

  isMobile: boolean = false;

  deparmtnets: Department[] = [];

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

  desktopColumnDefs: ColDef[] = [
    {
      field: 'DepartmentId',
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
        onEditClick: (data: any) => this.requestDepartmentProcess(data),
        onDeleteClick: (data: any) => this.deleteDepartment(data)
      },
      cellClass: 'text-center'
    }
  ];

  mobileColumnDefs: ColDef[] = [
    {
      field: 'Name',
      headerName: 'Name',
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
        onEditClick: (data: any) => this.requestDepartmentProcess(data)
      },
      cellClass: 'text-center'
    }
  ];

  showSidebar: boolean = false;

  selectedDepartment: Department | null = null;


  constructor(private departmentService: DepartmentService,
    private loader: LoaderService,
    private toster: ToastrService,
    private audit: AuditFieldsService) { }
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


  ngOnInit(): void {
    this.checkScreenSize();
    this.setupResponsiveColumns();
    this.loadDepartmentsData();
    window.addEventListener('resize', this.onResize.bind(this));
  }
  loadDepartmentsData(): void {
    this.loader.show();

    this.departmentService.getDepartmentsListAsync().subscribe({
      next: (deparmtnetResponse: Department[]) => {
        this.deparmtnets = deparmtnetResponse;
        this.loader.hide();
        if (this.gridApi) {
          setTimeout(() => {
            this.gridApi.sizeColumnsToFit();
          }, 100);
        }
      },
      error: (error) => {
        console.error('Error loading roles:', error);
        this.loader.hide();

        this.toster.error('Failed to load roles', 'Error');
      }
    });
  }

  onGridReady(params: GridReadyEvent): void {
    this.gridApi = params.api;
    setTimeout(() => {
      this.gridApi.sizeColumnsToFit();
    }, 300);
  }

  deleteDepartment(department: Department): void {

  }
  requestDepartmentProcess(department: Department): void {

  }
  openAddDepartment(): void {
    this.showSidebar = true;
  }

  onCloseSidebar(): void {
    this.showSidebar = false;
  }
  OnSaveDepartment(department: Department): void {
    this.loader.show();
    var _deparmtnent = this.audit.appendAuditFields(department);
    console.log(JSON.stringify(_deparmtnent));
    this.loader.hide();
  }
  getTotalRowsCount(): number {
    return this.deparmtnets.length;
  }
  getActiveDeparmtnetsCount(): number {
    return this.deparmtnets.filter(c => c.IsActive).length;
  }
  getInActiveDeparmtnetsCount(): number {
    return this.deparmtnets.filter(c => !c.IsActive).length;
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

}

