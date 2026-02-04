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
import { RoleService } from '../../../services/role.service';
import { DepartmentService } from '../../../services/department.service';
import { DesignationService } from '../../../services/designation.service';
import { ToastrService } from 'ngx-toastr';
import { AuditFieldsService } from '../../../../common/services/auditfields.service';
import { LoaderService } from '../../../../common/services/loader.service';
import { EmployeesDetails } from '../../../models/employees.details';
import { forkJoin } from 'rxjs';
import { EmployeeActionComponent } from './employee-action-component';
import { Employee } from '../../../models/employee';
import { MobileEmployeeActionComponent } from './mobile-employee-action.component';

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
  employees: EmployeesDetails[] = [];
  columnDefs: ColDef[] = [];

  // Cache for lookup data
  private rolesMap: Map<number, string> = new Map();
  private departmentsMap: Map<number, string> = new Map();
  private designationsMap: Map<number, string> = new Map();

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
      width: 150,
      sortable: true,
      filter: 'agTextColumnFilter',
      cellRenderer: this.employeeInfoRenderer.bind(this),
      comparator: this.employeeComparator.bind(this),
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
      field: 'DesignationName',
      headerName: 'Designation',
      width: 150,
      filter: 'agTextColumnFilter',
      sortable: true,
      valueGetter: (params) => {
        return params.data.DesignationName || this.getDesignationName(params.data.DesignationId);
      }
    },
    {
      field: 'CurrentPrice',
      headerName: 'Current Salary',
      width: 120,
      filter: 'agNumberColumnFilter',
      sortable: true,
      valueFormatter: this.currencyFormatter.bind(this),
      cellClass: 'text-right'
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
      cellRenderer: EmployeeActionComponent, // Use the new component
      cellRendererParams: {
        onDetailsClick: (data: any) => this.viewEmployeeDetails(data),
        onCreateUserClick: (data: any) => this.createUserAccess(data),
        onActivateClick: (data: any) => this.activateEmployee(data),
        onDeactivateClick: (data: any) => this.deactivateEmployee(data),
        onDeleteClick: (data: any) => this.deleteEmployee(data)
      },
      cellClass: 'text-center'
    }
  ];

  mobileColumnDefs: ColDef[] = [
    {
      headerName: 'Employee',
      width: 180,
      cellRenderer: this.mobileEmployeeInfoRenderer.bind(this),
      sortable: true,
      filter: 'agTextColumnFilter'
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
      field: 'IsActive',
      headerName: 'Status',
      width: 80,
      cellRenderer: this.mobileStatusRenderer.bind(this),
      cellClass: 'text-center',
      sortable: true,
      filter: 'agTextColumnFilter'
    },
    {
      field: 'Actions',
      headerName: '',
      width: 120,
      sortable: false,
      filter: false,
      cellRenderer: MobileEmployeeActionComponent,
      cellRendererParams: {
        onDetailsClick: (data: any) => this.viewEmployeeDetails(data),
        onCreateUserClick: (data: any) => this.createUserAccess(data),
        onActivateClick: (data: any) => this.activateEmployee(data),
        onDeactivateClick: (data: any) => this.deactivateEmployee(data),
        onDeleteClick: (data: any) => this.deleteEmployee(data)
      },
      cellClass: 'text-center'
    }
  ];
  constructor(
    private employeeService: EmployeeService,
    private roleService: RoleService,
    private departmentService: DepartmentService,
    private designationService: DesignationService,
    private toastr: ToastrService,
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
    this.loadInitialData(); // Load all data initially using forkJoin
  }

  // Initial load - fetch all data using forkJoin
  private loadInitialData(): void {
    this.loader.show();

    forkJoin({
      roles: this.roleService.getRoleListAsync(),
      departments: this.departmentService.getDepartmentsListAsync(),
      designations: this.designationService.getDesignationsListAsync(),
      employees: this.employeeService.getEmployeesListAsync()
    }).subscribe({
      next: ({ roles, departments, designations, employees }) => {
        // Process roles
        this.rolesMap.clear();
        roles.forEach(role => {
          this.rolesMap.set(role.Id, role.Name);
        });

        // Process departments
        this.departmentsMap.clear();
        departments.forEach(dept => {
          this.departmentsMap.set(dept.DepartmentId, dept.Name);
        });

        // Process designations
        this.designationsMap.clear();
        designations.forEach(designation => {
          this.designationsMap.set(designation.DesignationId, designation.Name);
        });

        // Process and map employees with lookup data
        this.employees = employees.map(emp => {
          const employeeDetail: EmployeesDetails = {
            ...emp,
            DeparmtnetName: this.getDepartmentName(emp.DepartmentId ?? null),
            DesignationName: this.getDesignationName(emp.DesignationId ?? null),
            RoleName: this.getRoleName(emp.RoleId ?? null)
          };
          return employeeDetail;
        });

        this.loader.hide();
        // Update grid if ready
        if (this.gridApi) {
          setTimeout(() => {
            this.gridApi.sizeColumnsToFit();
          }, 100);
        }
      },
      error: (error) => {
        console.error('Error loading initial data:', error);
        this.loader.hide();
        this.toastr.error('Failed to load data');
      }
    });
  }


  viewEmployeeDetails(employee: Employee): void {

  }
  createUserAccess(employee: Employee): void {

  }
  activateEmployee(employee: Employee): void {

  }
  deactivateEmployee(employee: Employee): void {

  }
  // Refresh only employee data
  refreshEmployeeData(): void {
    this.loader.show();
    this.employeeService.getEmployeesListAsync().subscribe({
      next: (employees) => {
        // Map employees with existing lookup data
        this.employees = employees.map(emp => {
          const employeeDetail: EmployeesDetails = {
            ...emp,
            DeparmtnetName: this.getDepartmentName(emp.DepartmentId ?? null),
            DesignationName: this.getDesignationName(emp.DesignationId ?? null),
            RoleName: this.getRoleName(emp.RoleId ?? null)
          };
          return employeeDetail;
        });

        this.loader.hide();
        this.toastr.success('Employee data refreshed');

        // Update grid
        if (this.gridApi) {
          setTimeout(() => {
            this.gridApi.sizeColumnsToFit();
          }, 100);
        }
      },
      error: (error) => {
        this.toastr.error('Failed to refresh employee data');
        this.loader.hide();
        console.error('Error refreshing employee data:', error);
      }
    });
  }

  // Refresh only lookup data (roles, departments, designations)
  refreshLookupData(): void {
    this.loader.show();

    forkJoin({
      roles: this.roleService.getRoleListAsync(),
      departments: this.departmentService.getDepartmentsListAsync(),
      designations: this.designationService.getDesignationsListAsync()
    }).subscribe({
      next: ({ roles, departments, designations }) => {
        // Process roles
        this.rolesMap.clear();
        roles.forEach(role => {
          this.rolesMap.set(role.Id, role.Name);
        });

        // Process departments
        this.departmentsMap.clear();
        departments.forEach(dept => {
          this.departmentsMap.set(dept.DepartmentId, dept.Name);
        });

        // Process designations
        this.designationsMap.clear();
        designations.forEach(designation => {
          this.designationsMap.set(designation.DesignationId, designation.Name);
        });

        this.loader.hide();
        this.toastr.success('Reference data refreshed');

        // Re-map employees with updated lookup data
        this.mapEmployeesWithUpdatedLookup();
      },
      error: (error) => {
        console.error('Error refreshing lookup data:', error);
        this.loader.hide();
        this.toastr.error('Failed to refresh reference data');
      }
    });
  }

  // Helper method to map employees with updated lookup data
  private mapEmployeesWithUpdatedLookup(): void {
    if (this.employees.length > 0) {
      this.employees = this.employees.map(emp => {
        const employeeDetail: EmployeesDetails = {
          ...emp,
          DeparmtnetName: this.getDepartmentName(emp.DepartmentId ?? null),
          DesignationName: this.getDesignationName(emp.DesignationId ?? null),
          RoleName: this.getRoleName(emp.RoleId ?? null)
        };
        return employeeDetail;
      });

      // Update grid
      if (this.gridApi) {
        this.gridApi.sizeColumnsToFit();
      }
    }
  }

  // Helper methods to get names from maps
  private getRoleName(roleId: number | null | undefined): string {
    if (roleId === null || roleId === undefined) return 'N/A';
    return this.rolesMap.get(roleId) || 'Unknown Role';
  }

  private getDepartmentName(departmentId: number | null | undefined): string {
    if (departmentId === null || departmentId === undefined) return 'N/A';
    return this.departmentsMap.get(departmentId) || 'Unknown Department';
  }

  private getDesignationName(designationId: number | null | undefined): string {
    if (designationId === null || designationId === undefined) return 'N/A';
    return this.designationsMap.get(designationId) || 'Unknown Designation';
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

  // Custom renderer for employee info with gender icon
  employeeInfoRenderer(params: ICellRendererParams): string {
    const gender = params.data.Gender;
    const isMale = gender === 'Male' || gender === 'M';
    const genderIcon = isMale ? 'mdi-human-male text-primary' : 'mdi-human-female text-pink';
    const employeeCode = params.data.EmployeeCode || 'N/A';

    return `
    <div class="d-flex align-items-center" style="white-space: nowrap;">
      <i class="mdi ${genderIcon} mdi-24px mr-2"></i>
      <div>
        <div class="d-flex align-items-center gap-2">
          <span><strong>${employeeCode}</strong></span>
        </div>
      </div>
    </div>
  `;
  }

  // Mobile version of employee info renderer
  mobileEmployeeInfoRenderer(params: ICellRendererParams): string {
    const gender = params.data.Gender;
    const isMale = gender === 'Male' || gender === 'M';
    const genderIcon = isMale ? 'mdi-human-male text-primary' : 'mdi-human-female text-pink';
    const employeeCode = params.data.EmployeeCode || 'N/A';

    return `
    <div class="d-flex align-items-center" style="white-space: nowrap;">
      <i class="mdi ${genderIcon} mdi-24px mr-2"></i>
      <div>
        <div class="d-flex align-items-center gap-2">
          <span><strong>${employeeCode}</strong></span>
        </div>
      </div>
    </div>
  `;
  }
  // Comparator for sorting by gender and employee code
  employeeComparator(valueA: any, valueB: any, nodeA: any, nodeB: any): number {
    const dataA = nodeA.data;
    const dataB = nodeB.data;

    // First compare by gender (Male first)
    const genderA = dataA.Gender || '';
    const genderB = dataB.Gender || '';

    if (genderA === 'Male' && genderB !== 'Male') return -1;
    if (genderA !== 'Male' && genderB === 'Male') return 1;

    // Then compare by employee code
    const codeA = dataA.EmployeeCode || '';
    const codeB = dataB.EmployeeCode || '';

    return codeA.localeCompare(codeB);
  }

  statusCellClass(params: any): string {
    const isActive = params.value;
    return isActive ? 'status-active' : 'status-inactive';
  }

  currencyFormatter(params: ValueFormatterParams): string {
    if (!params.value && params.value !== 0) return 'N/A';

    const amount = parseFloat(params.value);
    if (isNaN(amount)) return 'Invalid';

    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(amount);
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
    return this.employees.length;
  }

  getActiveEmployeesCount(): number {
    return this.employees.filter(e => e.IsActive).length;
  }

  getInactiveEmployeesCount(): number {
    return this.employees.filter(e => !e.IsActive).length;
  }

  editEmployee(employee: EmployeesDetails): void {
    console.log('Edit employee:', employee);
    // Implement edit logic
  }

  deleteEmployee(employee: EmployeesDetails): void {
    if (confirm(`Are you sure you want to delete ${employee.FirstName} ${employee.LastName}?`)) {
      // this.employeeService.deleteEmployee(employee.EmployeeId).subscribe({
      //   next: () => {
      //     this.toastr.success('Employee deleted successfully');
      //     this.refreshEmployeeData();
      //   },
      //   error: (error) => {
      //     this.toastr.error('Failed to delete employee');
      //     console.error('Error deleting employee:', error);
      //   }
      // });
    }
  }
}