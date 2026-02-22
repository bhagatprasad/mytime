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
import { RoleService } from '../../../services/role.service';
import { Role } from '../../../models/role';
import { ToastrService } from 'ngx-toastr';
import { LoaderService } from '../../../../common/services/loader.service';
import { CreateRoleComponent } from './create-role.component';
import { AuditFieldsService } from '../../../../common/services/auditfields.service';
import { ActionsRendererComponent } from '../../../../common/components/actions-renderer.component';
import { MobileActionsRendererComponent } from '../../../../common/components/mobile-actions-renderer.component';
import { DeleteConfirmationComponent } from '../../../../common/components/delete.compunent';

// Register AG Grid modules
ModuleRegistry.registerModules([AllCommunityModule]);

@Component({
  selector: 'app-role',
  standalone: true,
  imports: [CommonModule, AgGridAngular, DatePipe, FormsModule, CreateRoleComponent,DeleteConfirmationComponent],
  templateUrl: './role.component.html',
  styleUrls: ['./role.component.css']
})
export class RoleComponent implements OnInit, OnDestroy {

  today = new Date();
  // Grid API
  private gridApi!: GridApi;

  // Responsive state
  isMobile: boolean = false;

  showDeletePopup = false;

  selectedDeleteItem: Role | null = null;


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
      width: 120,
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
        onEditClick: (data: any) => this.requestRoleProcess(data),
        onDeleteClick: (data: any) => this.deleteRole(data)
      },
      cellClass: 'text-center'
    }
  ];

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
      field: 'Actions',
      headerName: '',
      width: 80,
      sortable: false,
      filter: false,
      cellRenderer: MobileActionsRendererComponent,
      cellRendererParams: {
        onEditClick: (data: any) => this.requestRoleProcess(data)
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

  rowData: Role[] = [];

  isLoading: boolean = false;

  showSidebar: boolean = false;
  selectedRole: Role | null = null;

  constructor(
    private roleService: RoleService,
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

    this.roleService.getRoleListAsync().subscribe({
      next: (roles: Role[]) => {
        this.rowData = roles;
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

        this.toastr.error('Failed to load roles', 'Error');
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
    return this.rowData.filter(role => role.IsActive).length;
  }

  getInactiveRolesCount(): number {
    return this.rowData.filter(role => !role.IsActive).length;
  }
  deleteRole(role: Role): void {
    this.selectedDeleteItem = role;
    this.showDeletePopup = true;
    console.log(JSON.stringify(role));
  }

  closePopup(): void {
    this.showDeletePopup = false;
    this.selectedDeleteItem = null;
  }

  requestRoleProcess(role: Role): void {
    this.selectedRole = role;
    this.showSidebar = true;
  }
  openAddEditRole(): void {
    this.selectedRole = null;
    this.showSidebar = true;
  }
  onSaveRole(role: Role): void {
    this.loader.show();
    var _role = this.audit.appendAuditFields(role);
    console.log("we have receved role data " + JSON.stringify(role));
    this.roleService.saveRoleAsync(_role).subscribe(
      reponse => {
        if (reponse) {
          this.toastr.success("Role processed succeessfully");
          this.showSidebar = false;
          this.refreshData();
        }
      }, error => {
        this.toastr.error("something went wrong , please check and resubmit");
        this.showSidebar = true;
        this.loader.hide();
      });

  }
  onCloseSidebar(): void {
    this.showSidebar = false;
  }

  deleterole(){

    if (!this.selectedDeleteItem) {
      console.error("No item selected for delete");
      return;
    }

    this.roleService.deleteRoleAsync(this.selectedDeleteItem.Id)
      .subscribe({
        next: (res) => {
          console.log("Delete success:", res);

          this.refreshData();          // reload grid data
          this.showDeletePopup = false;
          this.selectedDeleteItem = null;
        },
        error: (err) => {
          console.error("Delete failed:", err);
          // keep popup open OR close — your choice
          this.showDeletePopup = false;
        },
        complete: () => {
          alert("Delete request completed");
        }
      });
    }
}