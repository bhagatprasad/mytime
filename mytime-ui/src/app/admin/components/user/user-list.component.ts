import { Component, HostListener, OnDestroy, OnInit } from '@angular/core';
import { AllCommunityModule, ColDef, GridApi, GridOptions, GridReadyEvent, ICellRendererParams, ModuleRegistry } from 'ag-grid-community';
import { User } from '../../models/user';
import { UserDeetails } from '../../models/user-detail';
import { Department } from '../../models/department';
import { Role } from '../../models/role';
import { UserService } from '../../services/user.service';
import { RoleService } from '../../services/role.service';
import { DepartmentService } from '../../services/department.service';
import { ToastrService } from 'ngx-toastr';
import { LoaderService } from '../../../common/services/loader.service';
import { AuditFieldsService } from '../../../common/services/auditfields.service';
import { CommonModule } from '@angular/common';
import { AgGridAngular } from 'ag-grid-angular';
import { forkJoin } from 'rxjs';
import { UserActionComponent } from './user-action.component';
import { MobileUserActionComponent } from './mobile-user-action.component';

ModuleRegistry.registerModules([AllCommunityModule]);


@Component({
  selector: 'app-user-list',
  standalone: true,
  imports: [CommonModule, AgGridAngular],
  templateUrl: './user-list.component.html',
  styleUrl: './user-list.component.css'
})
export class UserListComponent implements OnInit, OnDestroy {

  today = new Date();

  private gridApi!: GridApi;

  isMobile: boolean = false;

  columnDefs: ColDef[] = [];

  users: User[] = [];

  userDeetails: UserDeetails[] = [];

  selectedUser: User | null = null;

  coreRoles: Role[] = [];

  coreDepartments: Department[] = [];

  private rolesMap: Map<number, string> = new Map();

  private departmentsMap: Map<number, string> = new Map();

  showSidebar: boolean = false;

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
      headerName: 'Employee',
      field: 'EmployeeId',
      width: 150,
      sortable: true,
      filter: 'agTextColumnFilter',
      cellClass: 'text-left'
    },
    {
      field: 'FirstName',
      headerName: 'Full Name',
      width: 180,
      filter: 'agTextColumnFilter',
      sortable: true,
      valueGetter: (params) => {
        return `${params.data.FirstName || ''} ${params.data.LastName || ''}`.trim();
      }
    },
    {
      field: 'Email',
      headerName: 'Email',
      width: 200,
      filter: 'agTextColumnFilter',
      sortable: true
    },
    {
      field: 'Phone',
      headerName: 'Phone',
      width: 120,
      filter: 'agTextColumnFilter',
      sortable: true,
      cellClass: 'text-center'
    },
    {
      field: 'RoleName',
      headerName: 'Role',
      width: 120,
      filter: 'agTextColumnFilter',
      sortable: true,
      valueGetter: (params) => {
        return params.data.RoleName || this.getRoleName(params.data.RoleId);
      },
      cellClass: 'text-center'
    },
    {
      field: 'DepartmentName',
      headerName: 'Department',
      width: 150,
      filter: 'agTextColumnFilter',
      sortable: true,
      valueGetter: (params) => {
        return params.data.DepartmentName || this.getDepartmentName(params.data.DepartmentId);
      }
    },
    {
      field: 'IsActive',
      headerName: 'Status',
      width: 100,
      filter: 'agTextColumnFilter',
      sortable: true,
      cellRenderer: this.statusRenderer.bind(this),
      cellClass: this.statusCellClass.bind(this),
    },
    {
      field: 'Actions',
      headerName: 'Actions',
      width: 200,
      sortable: false,
      filter: false,
      cellRenderer: UserActionComponent,
      cellRendererParams: {
        onDetailsClick: (data: any) => this.onDetailsClick(data),
        onEditClick: (data: any) => this.onEditClick(data),
        onChangePasswordClick: (data: any) => this.onChangePasswordClick(data),
        onDeactivateClick: (data: any) => this.onDeactivateClick(data),
        onActivateClick: (data: any) => this.onActivateClick(data),
        onDeleteClick: (data: any) => this.onDeleteClick(data),
      },
      cellClass: 'text-center'
    }
  ];

  mobileColumnDefs: ColDef[] = [
    {
      field: 'FirstName',
      headerName: 'Full Name',
      width: 180,
      filter: 'agTextColumnFilter',
      sortable: true,
      valueGetter: (params) => {
        return `${params.data.FirstName || ''} ${params.data.LastName || ''}`.trim();
      }
    },
    {
      field: 'Actions',
      headerName: '',
      width: 120,
      sortable: false,
      filter: false,
      cellRenderer: MobileUserActionComponent,
      cellRendererParams: {
        onDetailsClick: (data: any) => this.onDetailsClick(data),
        onEditClick: (data: any) => this.onEditClick(data),
        onChangePasswordClick: (data: any) => this.onChangePasswordClick(data),
        onDeactivateClick: (data: any) => this.onDeactivateClick(data),
        onActivateClick: (data: any) => this.onActivateClick(data),
        onDeleteClick: (data: any) => this.onDeleteClick(data),
      },
      cellClass: 'text-center',
      pinned: 'right'
    }
  ];
  constructor(private userService: UserService,
    private roleService: RoleService,
    private departmentService: DepartmentService,
    private toster: ToastrService,
    private loader: LoaderService,
    private audit: AuditFieldsService
  ) {

  }
  ngOnDestroy(): void {
    window.removeEventListener('resize', this.onResize.bind(this));
  }

  ngOnInit(): void {
    this.checkScreenSize();
    this.setupResponsiveColumns();
    window.addEventListener('resize', this.onResize.bind(this));
    this.loadInitialData(); // Load all data initially using forkJoin
  }

  private loadInitialData(): void {
    this.loader.show();

    forkJoin({
      roles: this.roleService.getRoleListAsync(),
      departments: this.departmentService.getDepartmentsListAsync(),
      users: this.userService.GetAllUsersAsync()
    }).subscribe({
      next: ({ roles, departments, users }) => {
        this.coreRoles = roles;
        this.coreDepartments = departments;
        this.rolesMap.clear();
        roles.forEach(role => {
          this.rolesMap.set(role.Id, role.Name);
        });

        this.departmentsMap.clear();
        departments.forEach(dept => {
          this.departmentsMap.set(dept.DepartmentId, dept.Name);
        });

        this.userDeetails = users.map(user => {
          const userDeetails: UserDeetails = {
            ...user,
            DepartmentName: this.getDepartmentName(user.DepartmentId ?? null),
            RoleName: this.getRoleName(user.RoleId ?? null)
          };
          return userDeetails;
        });

        this.loader.hide();
        if (this.gridApi) {
          setTimeout(() => {
            this.gridApi.sizeColumnsToFit();
          }, 100);
        }
      },
      error: (error) => {
        console.error('Error loading initial data:', error);
        this.loader.hide();
        this.toster.error('Failed to load data');
      }
    });
  }
  refreshEmployeeData(): void {
    this.loader.show();
    this.userService.GetAllUsersAsync().subscribe({
      next: (users) => {
        this.users = users.map(emp => {
          const userDeetails: UserDeetails = {
            ...emp,
            DepartmentName: this.getDepartmentName(emp.DepartmentId ?? null),
            RoleName: this.getRoleName(emp.RoleId ?? null)
          };
          return userDeetails;
        });

        this.loader.hide();
        this.toster.success('Users data refreshed');

        if (this.gridApi) {
          setTimeout(() => {
            this.gridApi.sizeColumnsToFit();
          }, 100);
        }
      },
      error: (error) => {
        this.toster.error('Failed to refresh users data');
        this.loader.hide();
        console.error('Error refreshing users data:', error);
      }
    });
  }

  refreshLookupData(): void {
    this.loader.show();

    forkJoin({
      roles: this.roleService.getRoleListAsync(),
      departments: this.departmentService.getDepartmentsListAsync(),
    }).subscribe({
      next: ({ roles, departments }) => {
        this.rolesMap.clear();
        roles.forEach(role => {
          this.rolesMap.set(role.Id, role.Name);
        });

        this.departmentsMap.clear();
        departments.forEach(dept => {
          this.departmentsMap.set(dept.DepartmentId, dept.Name);
        });

        this.loader.hide();
        this.toster.success('Reference data refreshed');
        this.mapUsersWithUpdatedLookup();
      },
      error: (error) => {
        console.error('Error refreshing lookup data:', error);
        this.loader.hide();
        this.toster.error('Failed to refresh reference data');
      }
    });
  }
  private mapUsersWithUpdatedLookup(): void {
    if (this.users.length > 0) {
      this.userDeetails = this.users.map(user => {
        const userDeetails: UserDeetails = {
          ...user,
          DepartmentName: this.getDepartmentName(user.DepartmentId ?? null),
          RoleName: this.getRoleName(user.RoleId ?? null)
        };
        return userDeetails;
      });

      if (this.gridApi) {
        this.gridApi.sizeColumnsToFit();
      }
    }
  }
  private getRoleName(roleId: number | null | undefined): string {
    if (roleId === null || roleId === undefined) return 'N/A';
    return this.rolesMap.get(roleId) || 'Unknown Role';
  }

  private getDepartmentName(departmentId: number | null | undefined): string {
    if (departmentId === null || departmentId === undefined) return 'N/A';
    return this.departmentsMap.get(departmentId) || 'Unknown Department';
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
  mobileStatusRenderer(params: ICellRendererParams): string {
    const isActive = params.value;
    const statusText = isActive ? 'Active' : 'Inactive';
    const statusClass = isActive ? 'success' : 'danger';

    return `<span class="badge bg-${statusClass}">${statusText}</span>`;
  }

  // Public methods for refreshing
  refreshData(): void {
    this.refreshEmployeeData();
  }

  refreshAllData(): void {
    this.loadInitialData();
  }

  getSelectedRowsCount(): number {
    return this.gridApi?.getSelectedRows()?.length || 0;
  }

  getTotalRowsCount(): number {
    return this.userDeetails.length;
  }

  getActiveUserCount(): number {
    return this.userDeetails.filter(e => e.IsActive).length;
  }

  getInactiveUserCount(): number {
    return this.userDeetails.filter(e => !e.IsActive).length;
  }
  openAddEditUser(): void {
    this.showSidebar = true;
    this.selectedUser = null;
  }
  onDetailsClick(user: User): void {

  }
  onEditClick(user: User): void {

  }
  onChangePasswordClick(user: User): void {

  }
  onDeactivateClick(user: User): void {

  }
  onActivateClick(user: User): void {

  }
  onDeleteClick(user: User): void {

  }
}
