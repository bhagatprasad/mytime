import { CommonModule, DatePipe } from '@angular/common';
import { Component, OnDestroy, OnInit, HostListener } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { AgGridAngular } from 'ag-grid-angular';
import { 
  AllCommunityModule, 
  ColDef, 
  GridApi, 
  GridOptions, 
  ICellRendererParams, 
  ModuleRegistry, 
  ValueFormatterParams,
  GridReadyEvent 
} from 'ag-grid-community';
import { EmployeeService } from '../../../services/employee.service';
import { ToastrService } from 'ngx-toastr';
import { AuditFieldsService } from '../../../../common/services/auditfields.service';
import { LoaderService } from '../../../../common/services/loader.service';
import { ActionsRendererComponent } from '../../../../common/components/actions-renderer.component';
import { Employee } from '../../../models/employee';

ModuleRegistry.registerModules([AllCommunityModule]);

@Component({
  selector: 'app-employees-list',
  standalone: true,
  imports: [CommonModule, AgGridAngular, FormsModule],
  templateUrl: './employees-list.component.html',
  styleUrls: ['./employees-list.component.css']
})
export class EmployeesListComponent implements OnInit, OnDestroy {

  today = new Date();
  private gridApi!: GridApi;
  isMobile: boolean = false;
  employees: Employee[] = [];
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
      field: 'EmployeeId',
      headerName: 'ID',
      width: 80,
      filter: 'agNumberColumnFilter',
      sortable: true,
      cellClass: 'text-center'
    },
    {
      field: 'FirstName',
      headerName: 'First Name',
      width: 120,
      filter: 'agTextColumnFilter',
      sortable: true,
      valueGetter: (params) => {
        return `${params.data.FirstName || ''} ${params.data.LastName || ''}`.trim();
      }
    },
    {
      field: 'EmployeeCode',
      headerName: 'Employee Code',
      width: 120,
      filter: 'agTextColumnFilter',
      sortable: true,
      cellClass: 'text-center'
    },
    {
      field: 'Email',
      headerName: 'Email',
      width: 180,
      filter: 'agTextColumnFilter',
      sortable: true
    },
    {
      field: 'Phone',
      headerName: 'Phone',
      width: 120,
      filter: 'agTextColumnFilter',
      sortable: true
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
        onEditClick: (data: any) => this.editEmployee(data),
        onDeleteClick: (data: any) => this.deleteEmployee(data)
      },
      cellClass: 'text-center'
    }
  ];

  mobileColumnDefs: ColDef[] = [
    {
      field: 'FirstName',
      headerName: 'Employee',
      width: 180,
      cellRenderer: this.mobileNameRenderer.bind(this)
    },
    {
      field: 'EmployeeCode',
      headerName: 'Code',
      width: 100,
      cellClass: 'text-center'
    },
    {
      field: 'IsActive',
      headerName: 'Status',
      width: 80,
      cellRenderer: this.mobileStatusRenderer.bind(this),
      cellClass: 'text-center'
    },
    {
      field: 'Actions',
      headerName: '',
      width: 80,
      sortable: false,
      filter: false,
      cellRenderer: ActionsRendererComponent, // Assuming you have a mobile version
      cellRendererParams: {
        onEditClick: (data: any) => this.editEmployee(data),
        onDeleteClick: (data: any) => this.deleteEmployee(data)
      },
      cellClass: 'text-center'
    }
  ];

  constructor(
    private employeeService: EmployeeService,
    private toastr: ToastrService, // Fixed typo
    private audit: AuditFieldsService,
    private loader: LoaderService
  ) { }

  ngOnDestroy(): void {
    window.removeEventListener('resize', this.onResize.bind(this));
  }

  ngOnInit(): void {
    this.checkScreenSize();
    this.setupResponsiveColumns();
    window.addEventListener('resize', this.onResize.bind(this));
    this.loadEmployees(); // Added method call
  }

  onGridReady(params: GridReadyEvent): void {
    this.gridApi = params.api;
    setTimeout(() => {
      this.gridApi.sizeColumnsToFit();
    }, 300);
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
    this.gridApi.setGridOption('columnDefs', this.columnDefs);
    setTimeout(() => {
      this.gridApi.refreshHeader();
      this.gridApi.sizeColumnsToFit();
    }, 100);
  }

  private loadEmployees(): void {
    this.loader.show();
    this.employeeService.getEmployeesListAsync().subscribe({
      next: (response) => {
        this.employees = response;
        if (this.gridApi) {
          this.gridApi.sizeColumnsToFit();
        }
        this.loader.hide();
      },
      error: (error) => {
        this.toastr.error('Failed to load employees');
        this.loader.hide();
        console.error('Error loading employees:', error);
      }
    });
  }

  nameRenderer(params: ICellRendererParams): string {
    return `
        <div class="employee-name-cell">
          <strong>${params.data.FirstName || ''} ${params.data.LastName || ''}</strong>
          <div class="text-muted small">${params.data.EmployeeCode || 'N/A'}</div>
        </div>
      `;
  }

  mobileNameRenderer(params: ICellRendererParams): string {
    return `
        <div class="mobile-employee-cell">
          <strong>${params.data.FirstName || ''} ${params.data.LastName || ''}</strong>
          <div class="text-muted small">${params.data.EmployeeCode || 'N/A'}</div>
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

  getSelectedRowsCount(): number {
    return this.gridApi?.getSelectedRows()?.length || 0;
  }

  getTotalRowsCount(): number {
    return this.employees.length;
  }

  getActiveEmployeesCount(): number {
    return this.employees.filter(e => e.IsActive).length;
  }

  getInactiveEmployeesCount(): number {
    return this.employees.filter(e => !e.IsActive).length;
  }

  editEmployee(employee: Employee): void {
    // Implement edit logic
    console.log('Edit employee:', employee);
  }

  deleteEmployee(employee: Employee): void {
  
   
  }
}
