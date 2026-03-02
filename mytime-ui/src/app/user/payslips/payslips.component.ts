import { Component, HostListener, OnInit } from '@angular/core';
import { EmployeeSalaryService } from '../../admin/services/employee_salary.service';
import { LoaderService } from '../../common/services/loader.service';
import { EmployeeSalary } from '../../admin/models/employee_salary';
import { CommonModule } from '@angular/common';
import { AccountService } from '../../common/services/account.service';
import { AllCommunityModule, ColDef, GridApi, GridOptions, GridReadyEvent, ModuleRegistry } from 'ag-grid-community';
import { ToastrService } from 'ngx-toastr';
import { AgGridAngular } from 'ag-grid-angular';
import { Employee } from '../../admin/models/employee';
import { MonthlySalaryAddComponent } from '../../admin/components/salary/monthly-salary-add.component';
import { Router, RouterModule } from '@angular/router';
import { SalaryActionComponent } from '../../admin/components/salary/salary-action-component';
import { EmployeeService } from '../../admin/services/employee.service';
import { UserService } from '../../admin/services/user.service';

ModuleRegistry.registerModules([AllCommunityModule]);

@Component({
  selector: 'app-payslips',
  standalone: true,
  imports: [CommonModule, AgGridAngular, MonthlySalaryAddComponent, RouterModule],
  templateUrl: './payslips.component.html',
  styleUrl: './payslips.component.css'
})
export class PayslipsComponent implements OnInit {

  today = new Date();

  employeeSalaries: EmployeeSalary[] = [];

  employees: Employee[] = [];

  isMobile: boolean = false;

  private gridApi!: GridApi;

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
    paginationPageSize: 20,
    paginationPageSizeSelector: [20, 40, 60, 100],
    rowSelection: 'single',
    animateRows: true,
    enableCellTextSelection: true,
    suppressRowClickSelection: false,
    domLayout: 'autoHeight'
  };

  desktopColumnDefs: ColDef[] = [

    {
      field: 'Title',
      headerName: 'Title',
      width: 200,
      filter: 'agTextColumnFilter',
      sortable: true,
      cellClass: 'text-center'
    },
    {
      field: 'SalaryYear',
      headerName: 'Salary (Month/Year)',
      width: 150,
      filter: 'agTextColumnFilter',
      sortable: true,
      cellClass: 'text-left',
      valueGetter: (params) => {
        return `${params.data.SalaryMonth}/${params.data.SalaryYear}`;
      }
    },
    {
      field: 'STDDAYS',
      headerName: 'Days(STD/WRK/LOP)',
      width: 120,
      filter: 'agTextColumnFilter',
      sortable: true,
      cellClass: 'text-left',
      valueGetter: (params) => {
        return `${params.data.STDDAYS}/${params.data.WRKDAYS}/${params.data.LOPDAYS}`;
      }
    },
    {
      field: 'NETTRANSFER',
      headerName: 'Amount(Net Pay)',
      width: 150,
      filter: 'agTextColumnFilter',
      sortable: true,
      cellClass: 'text-left',
      valueGetter: (params) => {
        return `${params.data.NETTRANSFER}`;
      }
    },
    {
      field: 'Earning_Montly_GROSSEARNINGS',
      headerName: 'Earnings(Gross / Deductions) Monthly',
      width: 150,
      filter: 'agTextColumnFilter',
      sortable: true,
      cellClass: 'text-left',
      valueGetter: (params) => {
        return `${params.data.Earning_Montly_GROSSEARNINGS}/${params.data.Deduction_Montly_GROSSSDeduction}`;
      }
    },
    {
      field: 'Earning_Montly_GROSSEARNINGS',
      headerName: 'Earnings(Gross / Deductions) Monthly',
      width: 150,
      filter: 'agTextColumnFilter',
      sortable: true,
      cellClass: 'text-left',
      valueGetter: (params) => {
        return `${params.data.Earning_Montly_GROSSEARNINGS}/${params.data.Earning_YTD_GROSSEARNINGS}`;
      }
    },
    {
      field: 'Deduction_Montly_GROSSSDeduction',
      headerName: 'Earnings(Gross / Deductions) Monthly',
      width: 150,
      filter: 'agTextColumnFilter',
      sortable: true,
      cellClass: 'text-left',
      valueGetter: (params) => {
        return `${params.data.Deduction_Montly_GROSSSDeduction}/${params.data.Deduction_YTD_GROSSSDeduction}`;
      }
    },
    {
      field: 'LOCATION',
      headerName: 'Location',
      width: 200,
      filter: 'agTextColumnFilter',
      sortable: true,
      cellClass: 'text-center'
    },
    {
      field: 'Actions',
      headerName: 'Actions',
      width: 200,
      sortable: false,
      filter: false,
      cellRenderer: SalaryActionComponent,
      cellRendererParams: {
        onEditClick: (data: any) => this.onEditClick(data),
        onDownloadClick: (data: any) => this.onDownloadClick(data),
        onDeleteClick: (data: any) => this.onDeleteClick(data),
      },
      cellClass: 'text-left'
    }
  ];


  mobileColumnDefs: ColDef[] = [
    {
      field: 'EmployeeId',
      headerName: 'Employee',
      width: 180,
      sortable: true,
      filter: 'agTextColumnFilter',
      valueGetter: (params) => {
        const employee = this.employees.find(e => e.EmployeeId === params.data.EmployeeId);
        return employee ? `(${employee.EmployeeCode}) ${employee.FirstName} ${employee.LastName}` : "Unknown Employee";
      }
    },
    {
      field: 'SalaryYear',
      headerName: 'Salary',
      width: 180,
      filter: 'agTextColumnFilter',
      sortable: true,
      cellClass: 'text-left',
      valueGetter: (params) => {
        return `${params.data.SalaryMonth}/${params.data.SalaryYear}`;
      }
    },
    {
      field: 'NETTRANSFER',
      headerName: 'Amount',
      width: 180,
      filter: 'agTextColumnFilter',
      sortable: true,
      cellClass: 'text-left',
      valueGetter: (params) => {
        return `${params.data.NETTRANSFER}/${params.data.Earning_Montly_GROSSEARNINGS}`;
      }
    }
  ];

  constructor(private employeeSalaryService: EmployeeSalaryService,
    private accountService: AccountService,
    private loader: LoaderService,
    private toster: ToastrService,
    private userService: UserService
  ) { }

  ngOnInit(): void {
    this.checkScreenSize();
    this.setupResponsiveColumns();
    window.addEventListener('resize', this.onResize.bind(this));

    this.loadLoggedInUserSalary()
  }

  loademployeesalary(id: any) {

    this.employeeSalaryService.getSalariesByEmployee(id)
      .subscribe({
        next: (res) => {
          console.log(res);
          this.employeeSalaries = res;
          this.loader.hide();
        },
        error: (err) => {
          this.toster.error('Error loading salary', err);
          this.loader.hide();
        }
      });
  }

  private loadLoggedInUserSalary(): void {
    this.loader.show();
    const user = this.accountService.getCurrentUser();

    if (!user) return;
    
    this.userService.GetUserByIdAsync(user.id).subscribe({
      next: (employee: any) => {
        this.loademployeesalary(employee.EmployeeId);
      }
    });
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
  ngOnDestroy(): void {
    window.removeEventListener('resize', this.onResize.bind(this));
  }
  onGridReady(params: GridReadyEvent): void {
    this.gridApi = params.api;
    setTimeout(() => {
      this.gridApi.sizeColumnsToFit();
    }, 300);
  }

  employeeInfoRenderer(params: any): string {
    const employeeId = params.data?.EmployeeId;

    if (!employeeId) {
      return '<span class="text-gray-400">—</span>';
    }

    const employee = this.employees.find(e => e.EmployeeId === employeeId);

    if (!employee) {
      return `<span class="text-gray-400">Unknown</span>`;
    }

    const employeeCode = employee.EmployeeCode || '';
    const firstName = employee.FirstName || '';
    const lastName = employee.LastName || '';
    const displayName = `(${employeeCode}) ${firstName} ${lastName}`.trim();

    // Use a span with click handler for Angular navigation
    return `<span class="employee-link" 
                   data-employee-id="${employeeId}"
                   style="text-decoration: none; color: #2196F3; cursor: pointer;"
                   title="Click to view employee details">
              ${displayName}
            </span>`;
  }

  employeeComparator(valueA: any, valueB: any, nodeA: any, nodeB: any, isInverted: boolean): number {
    const employeeA = this.employees.find(e => e.EmployeeId === nodeA.data?.EmployeeId);
    const employeeB = this.employees.find(e => e.EmployeeId === nodeB.data?.EmployeeId);

    const nameA = employeeA ? `(${employeeA.EmployeeCode}) ${employeeA.FirstName} ${employeeA.LastName}`.trim() : '';
    const nameB = employeeB ? `(${employeeB.EmployeeCode}) ${employeeB.FirstName} ${employeeB.LastName}`.trim() : '';

    return nameA.localeCompare(nameB);
  }

  getTotalRowsCount(): number {
    return this.employeeSalaries.length;
  }
  openAddSalary(): void {

  }

  getActiveEmployeesSalariesCount(): number {
    return this.employeeSalaries.filter(salary => salary.IsActive).length;
  }
  getInActiveEmployeesSalariesCount(): number {
    return this.employeeSalaries.filter(salary => !salary.IsActive).length;
  }

  private sortMonthlySalariesByYearDesc(salaries: any[]): any[] {
    return salaries.sort((a, b) => {
      if (a.SalaryYear > b.SalaryYear) return -1;
      if (a.SalaryYear < b.SalaryYear) return 1;
      return 0;
    });
  }

  getEmployeesCount(): number {
    const uniqueEmployeeIds = new Set(this.employeeSalaries.map(salary => salary.EmployeeId));
    return uniqueEmployeeIds.size;
  }
  onEditClick(salary: EmployeeSalary): void {
    //this.router.navigate(['/admin/salaries/edit', salary.EmployeeSalaryId]);
  }
  onDownloadClick(salary: EmployeeSalary): void {
    // Implement download logic here, e.g., call a service to get the file and trigger download
  }
  onDeleteClick(salary: EmployeeSalary): void {
    // Implement delete logic here, e.g., show confirmation dialog and call service to delete
  }
}
