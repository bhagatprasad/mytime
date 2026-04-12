import { CommonModule } from '@angular/common';
import {
  Component,
  HostListener,
  Inject,
  inject,
  OnDestroy,
  OnInit,
} from '@angular/core';
import { AgGridAngular } from 'ag-grid-angular';
import {
  AllCommunityModule,
  ColDef,
  GridApi,
  GridOptions,
  GridReadyEvent,
  ICellRendererParams,
  ModuleRegistry,
} from 'ag-grid-community';
import { AuditFieldsService } from '../../../common/services/auditfields.service';
import { LoaderService } from '../../../common/services/loader.service';
import { ToastrService } from 'ngx-toastr';
import { MonthlySalaryService } from '../../services/montly_salary.service';
import { MonthlySalary } from '../../models/monlty_salary';
import { ActionsRendererComponent } from '../../../common/components/actions-renderer.component';
import { MobileActionsRendererComponent } from '../../../common/components/mobile-actions-renderer.component';
import { MonthlySalaryAddComponent } from './monthly-salary-add.component';
import { MonthlySalaryDetails } from '../../models/monlty_salary.details';
import { EmployeeSalary } from '../../models/employee_salary';
import { RouterModule } from '@angular/router';
import { Employee } from '../../models/employee';
import { forkJoin } from 'rxjs';
import { EmployeeService } from '../../services/employee.service';

ModuleRegistry.registerModules([AllCommunityModule]);

@Component({
  selector: 'app-monthly-salary-list',
  standalone: true,
  imports: [
    CommonModule,
    AgGridAngular,
    MonthlySalaryAddComponent,
    RouterModule,
  ],
  templateUrl: './monthly-salary-list.component.html',
  styleUrl: './monthly-salary-list.component.css',
})
export class MonthlySalaryListComponent implements OnInit, OnDestroy {
  monthlySalaries: MonthlySalary[] = [];

  monthlySalaryDetails: MonthlySalaryDetails[] = [];

  employees: Employee[] = [];

  employeeSalaries: EmployeeSalary[] = [];

  today = new Date();

  private gridApi!: GridApi;

  isMobile: boolean = false;

  showDeletePopup = false;

  desktopColumnDefs: ColDef[] = [
    {
      field: 'Title',
      headerName: 'Title',
      cellRenderer: (params: any) => {
        return `<span class="text-primary" style="cursor:pointer;color:blue !Important" title="View employees">
                ${params.value}
              </span>`;
      },
      onCellClicked: (params: any) => {
        this.openEmployees(params.data.MonthlySalaryId);
      },
      width: 250,
      filter: 'agTextColumnFilter',
      sortable: true,
      cellClass: 'text-left',
    },
    {
      field: 'SalaryMonth',
      headerName: 'Month',
      width: 100,
      filter: 'agTextColumnFilter',
      sortable: true,
      cellClass: 'text-left',
    },
    {
      field: 'SalaryYear',
      headerName: 'Year',
      width: 100,
      filter: 'agTextColumnFilter',
      sortable: true,
      cellClass: 'text-left',
    },
    {
      field: 'Location',
      headerName: 'Location',
      width: 120,
      filter: 'agTextColumnFilter',
      sortable: true,
      cellClass: 'text-left',
    },
    {
      field: 'StdDays',
      headerName: 'StdDays',
      width: 80,
      filter: 'agTextColumnFilter',
      sortable: true,
      cellClass: 'text-left',
    },
    {
      field: 'WrkDays',
      headerName: 'WrkDays',
      width: 80,
      filter: 'agTextColumnFilter',
      sortable: true,
      cellClass: 'text-left',
    },
    {
      field: 'LopDays',
      headerName: 'LopDays',
      width: 80,
      filter: 'agTextColumnFilter',
      sortable: true,
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
    {
      field: 'Actions',
      headerName: 'Actions',
      width: 150,
      sortable: false,
      filter: false,
      cellRenderer: ActionsRendererComponent,
      cellRendererParams: {
        onEditClick: (data: any) => this.requestMonthlySalaryProcess(data),
        onDeleteClick: (data: any) => this.deleteMonthlySalary(data),
      },
      cellClass: 'text-left',
    },
  ];

  mobileColumnDefs: ColDef[] = [
    {
      field: 'Title',
      headerName: 'Title',
      width: 180,
      cellClass: 'text-left',
    },
    {
      field: 'SalaryYear',
      headerName: 'Salary(Month/Year)',
      width: 100,
      cellClass: 'text-left',
      valueGetter: (params) => {
        return `${params.data.SalaryMonth}/${params.data.SalaryYear}`;
      },
    },
    {
      field: 'Actions',
      headerName: '',
      width: 80,
      sortable: false,
      filter: false,
      cellRenderer: MobileActionsRendererComponent,
      cellRendererParams: {
        onEditClick: (data: any) => this.requestMonthlySalaryProcess(data),
        onDeleteClick: (data: any) => this.deleteMonthlySalary(data),
      },
      cellClass: 'text-left',
    },
  ];

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
    paginationPageSizeSelector: [10, 20, 50, 100],
    rowSelection: 'single',
    animateRows: true,
    enableCellTextSelection: true,
    suppressRowClickSelection: false,
    domLayout: 'autoHeight',
  };

  showSidebar: boolean = false;

  selectedMonthlySalary: MonthlySalary | null = null;

  showModal = false;
  selectedTitle = '';
  constructor(
    private monthlySalaryService: MonthlySalaryService,
    private employeesService: EmployeeService,
    private audit: AuditFieldsService,
    private loader: LoaderService,
    private toster: ToastrService,
  ) {}

  ngOnDestroy(): void {
    window.removeEventListener('resize', this.onResize.bind(this));
  }
  ngOnInit(): void {
    this.checkScreenSize();
    this.setupResponsiveColumns();
    this.loadInitalData();
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

  loadInitalData(): void {
    this.loader.show();
    forkJoin({
      employees: this.employeesService.getEmployeesListAsync(),
      monthlySalaries: this.monthlySalaryService.GetMonthlySalaryListAsync(),
    }).subscribe({
      next: (response) => {
        this.employees = response.employees;
        this.monthlySalaries = this.sortMonthlySalariesByYearDesc(
          response.monthlySalaries,
        );
        // this.monthlySalaryDetails = response; //this.sortMonthlySalariesByYearDesc(response);
        this.loader.hide();

        if (this.gridApi) {
          setTimeout(() => {
            this.gridApi.sizeColumnsToFit();
          }, 100);
        }
      },
      error: (error) => {
        this.toster.error(
          'Failed to load monthly salaries. Please try again later.',
          'Error',
        );
        this.loader.hide();
      },
    });
  }

  private sortMonthlySalariesByYearDesc(salaries: any[]): any[] {
    return salaries.sort((a, b) => {
      if (a.SalaryYear > b.SalaryYear) return -1;
      if (a.SalaryYear < b.SalaryYear) return 1;
      return 0;
    });
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

  refreshData(): void {
    this.loadInitalData();
  }

  openAddMonthlySalary(): void {
    this.selectedMonthlySalary = null;
    this.showSidebar = true;
  }
  onCloseSidebar(): void {
    this.showSidebar = false;
    this.selectedMonthlySalary = null;
  }

  onSaveMonthlySalary(monthlySalary: MonthlySalary): void {
    this.loader.show();

    const monthlySalaryData = this.audit.appendAuditFields(monthlySalary);

    this.monthlySalaryService
      .publishMonthlySalaryAsync(monthlySalaryData)
      .subscribe({
        next: (response: any) => {
          this.toster.success(
            'Monthly salary published successfully.',
            'Success',
          );
          this.onCloseSidebar();
          this.refreshData();
        },
        error: (error: any) => {
          this.toster.error(
            'Failed to publish monthly salary. Please try again later.',
            'Error',
          );
          this.loader.hide();
        },
      });
  }

  deleteMonthlySalary(monthlySalary: MonthlySalary): void {}

  openEmployees(id: number) {
    this.loader.show();

    this.monthlySalaryService.GetMonthlySalaryAsync(id).subscribe({
      next: (res) => {
        this.employeeSalaries = res.employee_salaries;
        this.showModal = true;
        this.loader.hide();
      },

      error: (err) => {
        this.toster.error('API Error:', err);
        this.loader.hide();
      },
    });
  }

  requestMonthlySalaryProcess(monthlySalary: MonthlySalary): void {
    this.selectedMonthlySalary = monthlySalary;
    this.showSidebar = true;
  }
  getTotalRowsCount(): number {
    return this.monthlySalaries.length;
  }

  getTotalEmployeesCount(): number {
    return this.employeeSalaries.length;
  }

  statusCellClass(params: any): string {
    const isActive = params.value;
    return isActive ? 'status-active' : 'status-inactive';
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

  getEmployeeDetails(employeeId: any): String | undefined {
    const employee = this.employees.find(
      (emp) => emp.EmployeeId === employeeId,
    );
    return employee
      ? `${employee.FirstName} ${employee.LastName}-(${employee.EmployeeCode})`
      : undefined;
  }
}
