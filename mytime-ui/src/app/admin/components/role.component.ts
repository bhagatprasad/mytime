import { Component, OnInit, OnDestroy, HostListener } from '@angular/core';
import { CommonModule, DatePipe } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AgGridAngular } from 'ag-grid-angular';
import {
  ColDef,
  GridApi,
  GridReadyEvent,
  GridOptions,
  ICellRendererParams,
  ValueFormatterParams,
  ModuleRegistry,
  AllCommunityModule
} from 'ag-grid-community';
import { RoleService } from '../services/role.service';
import { Role } from '../models/role';
import { ToastrService } from 'ngx-toastr';

// Register AG Grid modules
ModuleRegistry.registerModules([AllCommunityModule]);

@Component({
  selector: 'app-role',
  standalone: true,
  imports: [CommonModule, AgGridAngular, DatePipe, FormsModule],
  templateUrl: './role.component.html',
  styleUrls: ['./role.component.css']
})
export class RoleComponent implements OnInit, OnDestroy {

  today = new Date();
  // Grid API
  private gridApi!: GridApi;

  // Responsive state
  isMobile: boolean = false;

  // Desktop Columns (7-8 columns)
  desktopColumnDefs: ColDef[] = [
    {
      field: 'Id',
      headerName: 'ID',
      width: 80,
      filter: 'agNumberColumnFilter',
      sortable: true,
      cellClass: 'text-center'
    },
    {
      field: 'Name',
      headerName: 'Role Name',
      width: 200,
      filter: 'agTextColumnFilter',
      sortable: true,
      cellRenderer: this.nameRenderer.bind(this)
    },
    {
      field: 'Code',
      headerName: 'Role Code',
      width: 120,
      filter: 'agTextColumnFilter',
      sortable: true,
      cellClass: 'text-center'
    },
    {
      field: 'IsActive',
      headerName: 'Status',
      width: 100,
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
      width: 150,
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
      width: 150,
      filter: 'agDateColumnFilter',
      sortable: true,
      valueFormatter: this.dateFormatter.bind(this),
      cellClass: 'text-center'
    },
    {
      field: 'Actions',
      headerName: 'Actions',
      width: 120,
      sortable: false,
      filter: false,
      cellRenderer: this.actionsRenderer.bind(this),
      cellClass: 'text-center'
    }
  ];

  // Mobile Columns (Simplified view)
  mobileColumnDefs: ColDef[] = [
    {
      field: 'Name',
      headerName: 'Role',
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
      field: 'IsActive',
      headerName: 'Status',
      width: 100,
      cellRenderer: this.mobileStatusRenderer.bind(this),
      cellClass: this.statusCellClass.bind(this)
    },
    {
      field: 'Actions',
      headerName: '',
      width: 80,
      sortable: false,
      filter: false,
      cellRenderer: this.mobileActionsRenderer.bind(this),
      cellClass: 'text-center'
    }
  ];

  // Current columns based on screen size
  columnDefs: ColDef[] = [];

  // Default column definitions
  defaultColDef: ColDef = {
    flex: 1,
    minWidth: 100,
    filter: true,
    resizable: true,
    sortable: true,
    floatingFilter: false
  };

  // Grid options
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

  // Row Data from API
  rowData: Role[] = [];

  // Loading state
  isLoading: boolean = false;

  constructor(
    private roleService: RoleService,
    private toastr: ToastrService
  ) { }

  ngOnInit(): void {
    this.checkScreenSize();
    this.setupResponsiveColumns();
    this.loadRoleData();

    // Listen for window resize
    window.addEventListener('resize', this.onResize.bind(this));
  }

  ngOnDestroy(): void {
    window.removeEventListener('resize', this.onResize.bind(this));
  }

  // Check screen size
  @HostListener('window:resize', ['$event'])
  onResize(event: any): void {
    this.checkScreenSize();
  }

  private checkScreenSize(): void {
    const wasMobile = this.isMobile;
    this.isMobile = window.innerWidth < 768;

    // Only update if screen size category changed
    if (wasMobile !== this.isMobile) {
      this.setupResponsiveColumns();
    }
  }

  private setupResponsiveColumns(): void {
    if (this.isMobile) {
      // Mobile: Show simplified columns
      this.columnDefs = [...this.mobileColumnDefs];
      this.gridOptions.domLayout = 'autoHeight';
    } else {
      // Desktop: Show all columns
      this.columnDefs = [...this.desktopColumnDefs];
      this.gridOptions.domLayout = 'normal';
    }

    // Update grid if API exists
    if (this.gridApi) {
      this.refreshGridColumns();
    }
  }

  private refreshGridColumns(): void {
    if (!this.gridApi) return;

    // Create new reference for column definitions
    const newColumnDefs = JSON.parse(JSON.stringify(this.columnDefs));
    //this.gridApi.setColumnDefs(newColumnDefs);

    // Refresh grid
    setTimeout(() => {
      this.gridApi.refreshHeader();
      this.gridApi.sizeColumnsToFit();
    }, 100);
  }

  // Load data from service
  loadRoleData(): void {
    this.isLoading = true;

    this.roleService.getRoleListAsync().subscribe({
      next: (roles: Role[]) => {
        this.rowData = roles;
        this.isLoading = false;

        // Show success message
        this.toastr.success(`${roles.length} roles loaded successfully`, 'Success');

        // Refresh grid if API is available
        if (this.gridApi) {
          setTimeout(() => {
            this.gridApi.sizeColumnsToFit();
          }, 100);
        }
      },
      error: (error) => {
        console.error('Error loading roles:', error);
        this.isLoading = false;
        this.toastr.error('Failed to load roles', 'Error');

        // Show mock data for testing if API fails
        this.loadMockData();
      }
    });
  }

  // Mock data for testing
  private loadMockData(): void {
    const mockRoles: Role[] = [
      {
        Id: 1,
        Name: 'Administrator',
        Code: 'ADMIN',
        IsActive: true,
        CreatedBy: 1,
        CreatedOn: new Date('2023-01-15'),
        ModifiedBy: 1,
        ModifiedOn: new Date('2023-06-20')
      },
      {
        Id: 2,
        Name: 'Manager',
        Code: 'MGR',
        IsActive: true,
        CreatedBy: 1,
        CreatedOn: new Date('2023-02-10'),
        ModifiedBy: 2,
        ModifiedOn: new Date('2023-05-15')
      },
      {
        Id: 3,
        Name: 'Supervisor',
        Code: 'SUP',
        IsActive: true,
        CreatedBy: 2,
        CreatedOn: new Date('2023-03-05'),
        ModifiedBy: 2,
        ModifiedOn: new Date('2023-04-10')
      },
      {
        Id: 4,
        Name: 'User',
        Code: 'USER',
        IsActive: true,
        CreatedBy: 1,
        CreatedOn: new Date('2023-01-20'),
        ModifiedBy: 3,
        ModifiedOn: new Date('2023-03-25')
      },
      {
        Id: 5,
        Name: 'Guest',
        Code: 'GUEST',
        IsActive: false,
        CreatedBy: 1,
        CreatedOn: new Date('2023-02-28'),
        ModifiedBy: 1,
        ModifiedOn: new Date('2023-06-15')
      }
    ];

    this.rowData = mockRoles;
    this.toastr.info('Showing mock data for demonstration', 'Info');
  }

  // Grid ready event
  onGridReady(params: GridReadyEvent): void {
    this.gridApi = params.api;

    // Adjust column sizes after data is loaded
    setTimeout(() => {
      this.gridApi.sizeColumnsToFit();
    }, 300);
  }

  // Cell Renderers
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

  actionsRenderer(params: ICellRendererParams): string {
    return `
      <div class="d-flex justify-content-center gap-1">
        <button class="btn btn-sm btn-outline-primary" title="Edit">
          <i class="mdi mdi-pencil"></i>
        </button>
        <button class="btn btn-sm btn-outline-danger" title="Delete">
          <i class="mdi mdi-delete"></i>
        </button>
      </div>
    `;
  }

  mobileActionsRenderer(params: ICellRendererParams): string {
    return `
      <div class="d-flex justify-content-center">
        <button class="btn btn-sm btn-outline-primary" title="Edit">
          <i class="mdi mdi-dots-horizontal"></i>
        </button>
      </div>
    `;
  }

  statusCellClass(params: any): string {
    const isActive = params.value;
    return isActive ? 'status-active' : 'status-inactive';
  }

  // Date formatter
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
  // Export to CSV
  exportToCSV(): void {
    if (this.gridApi) {
      this.gridApi.exportDataAsCsv({
        fileName: `roles_${new Date().toISOString().split('T')[0]}.csv`,
        processCellCallback: (params) => {
          // Format dates for CSV export
          if (params.column.getColDef().field === 'CreatedOn' || 
              params.column.getColDef().field === 'ModifiedOn') {
            if (params.value) {
              return this.dateFormatter({ value: params.value } as ValueFormatterParams);
            }
          }
          if (params.column.getColDef().field === 'IsActive') {
            return params.value ? 'Active' : 'Inactive';
          }
          return params.value;
        }
      });
      this.toastr.success('Data exported to CSV successfully', 'Export Complete');
    }
  }

  // Refresh data
  refreshData(): void {
    this.loadRoleData();
  }

  // Add new role
  addNewRole(): void {
    this.toastr.info('Add new role functionality will be implemented', 'Coming Soon');
    // TODO: Implement modal/dialog for adding new role
    console.log('Add new role clicked');
  }

  // Get selected rows count
  getSelectedRowsCount(): number {
    return this.gridApi?.getSelectedRows()?.length || 0;
  }

  // Get total rows count
  getTotalRowsCount(): number {
    return this.rowData.length;
  }

  // Get active roles count
  getActiveRolesCount(): number {
    return this.rowData.filter(role => role.IsActive).length;
  }

  // Get inactive roles count
  getInactiveRolesCount(): number {
    return this.rowData.filter(role => !role.IsActive).length;
  }
}