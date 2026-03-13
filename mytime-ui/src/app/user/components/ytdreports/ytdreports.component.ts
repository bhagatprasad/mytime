import { Component, HostListener, OnInit, OnDestroy, ViewChild, ViewContainerRef } from '@angular/core';
import { EmployeeSalaryService } from '../../../admin/services/employee_salary.service';
import { LoaderService } from '../../../common/services/loader.service';
import { EmployeeSalary } from '../../../admin/models/employee_salary';
import { CommonModule } from '@angular/common';
import { AccountService } from '../../../common/services/account.service';
import { AllCommunityModule, ColDef, GridApi, GridOptions, GridReadyEvent, ModuleRegistry } from 'ag-grid-community';
import { ToastrService } from 'ngx-toastr';
import { AgGridAngular } from 'ag-grid-angular';
import { Employee } from '../../../admin/models/employee';
import { MonthlySalaryAddComponent } from '../../../admin/components/salary/monthly-salary-add.component';
import { Router, RouterModule } from '@angular/router';
import { EmployeeService } from '../../../admin/services/employee.service';
import { UserService } from '../../../admin/services/user.service';
import { UserActionComponent } from '../common/user-action-component';
import { UserMobileActionsComponent } from '../common/user-mobile-action-component';
import { PayslipPdfComponent } from '../../../common/components/payslip-pdf.component';
import { PayslipVM } from '../../../common/models/payslip';
import { EmployeeSalaryStructure } from '../../../admin/models/employee_salary_structure';
import { Department } from '../../../admin/models/department';
import { Designation } from '../../../admin/models/designation';
import { EmployeeSalaryStructureService } from '../../../admin/services/employee_salary_structure.service';
import { DesignationService } from '../../../admin/services/designation.service';
import { DepartmentService } from '../../../admin/services/department.service';
import { forkJoin } from 'rxjs';

ModuleRegistry.registerModules([AllCommunityModule]);

@Component({
  selector: 'app-ytdreports',
  standalone: true,
  imports: [CommonModule, AgGridAngular, MonthlySalaryAddComponent, RouterModule, PayslipPdfComponent],
  templateUrl: './ytdreports.component.html',
  styleUrl: './ytdreports.component.css'
})
export class YtdreportsComponent implements OnInit,OnDestroy {
  @ViewChild('payslipPdfContainer', { read: ViewContainerRef })
  payslipPdfContainer!: ViewContainerRef;

  today = new Date();
  employeeSalaries: EmployeeSalary[] = [];
  employee: Employee | null = null;
  employeeSalaryStructure: EmployeeSalaryStructure | null = null;
  employees: Employee[] = [];
  departments: Department[] = [];
  designations: Designation[] = [];
  isMobile: boolean = false;

  selectedPayslipData: PayslipVM | null = null;
  showPdfRenderer: boolean = false;
  pdfMode: 'download' | 'preview' = 'download';
  previewImageData: string | null = null;
  showPreviewModal: boolean = false;
  isPreviewLoading: boolean = false;

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
    {field:'SalaryYear', headerName: 'Month/Year', width: 110, filter: 'agTextColumnFilter', sortable: true, cellClass: 'text-center',valueGetter: (p) => `${p.data.SalaryMonth}/${p.data.SalaryYear}` },
    { field: 'Earning_YTD_Basic', headerName: 'Basic', width: 110, filter: 'agTextColumnFilter', sortable: true, cellClass: 'text-left' },
    { field: 'Earning_YTD_HRA', headerName: 'HRA', width: 110, filter: 'agTextColumnFilter', sortable: true, cellClass: 'text-left' },
    // { field: 'Earning_YTD_CONVEYANCE', headerName: 'CONVEYANCE', width: 100, filter: 'agTextColumnFilter', sortable: true, cellClass: 'text-left' },
    // { field: 'Earning_YTD_MEDICALALLOWANCE', headerName: 'MEDICALALLOWANCE', width: 100, filter: 'agTextColumnFilter', sortable: true, cellClass: 'text-left'},
    { field: 'Earning_YTD_SPECIALALLOWANCE', headerName: 'Special allowance', width: 110, filter: 'agTextColumnFilter', sortable: true, cellClass: 'text-left' },
    // { field: 'Earning_YTD_SPECIALBONUS', headerName: 'SPECIALBONUS', width: 100, filter: 'agTextColumnFilter', sortable: true, cellClass: 'text-left'},
    { field: 'Earning_YTD_STATUTORYBONUS', headerName: 'Bonus', width: 110, filter: 'agTextColumnFilter', sortable: true, cellClass: 'text-left' },
    { field: 'Earning_YTD_OTHERS', headerName: 'Others', width: 100, filter: 'agTextColumnFilter', sortable: true, cellClass: 'text-left' },
    { field: 'Earning_YTD_GROSSEARNINGS', headerName: 'Total Earning', width: 110, filter: 'agTextColumnFilter', sortable: true, cellClass: 'text-left' },
    { field: 'Deduction_YTD_PROFESSIONALTAX', headerName: 'Professional Tax', width: 110, filter: 'agTextColumnFilter', sortable: true, cellClass: 'text-left' },
    { field: 'Deduction_YTD_ProvidentFund', headerName: 'PF', width: 110, filter: 'agTextColumnFilter', sortable: true, cellClass: 'text-left' },
    { field: 'Deduction_YTD_GroupHealthInsurance', headerName: 'Health Insurance', width: 110, filter: 'agTextColumnFilter', sortable: true, cellClass: 'text-left' },
    // { field: 'Deduction_YTD_OTHERS', headerName: 'Others', width: 100, filter: 'agTextColumnFilter', sortable: true, cellClass: 'text-center' },
    { field: 'Deduction_YTD_GROSSSDeduction', headerName: 'Total Deduction', width: 110, filter: 'agTextColumnFilter', sortable: true, cellClass: 'text-left' },
    { field: 'Actions', headerName: 'Actions', width: 110, sortable: false, filter: false, cellRenderer: UserActionComponent, cellRendererParams: { onDownloadClick: (d: any) => this.onDownloadClick(d), onViewClick: (d: any) => this.onViewClick(d) }, cellClass: 'text-left' }
  ];

  mobileColumnDefs: ColDef[] = [
    { field: 'Earning_YTD_GROSSEARNINGS', headerName: 'Total Earning', width: 130, filter: 'agTextColumnFilter', sortable: true, cellClass: 'text-left' },
    { field: 'Deduction_YTD_GROSSSDeduction', headerName: 'Total Deduction', width: 130, filter: 'agTextColumnFilter', sortable: true, cellClass: 'text-center' },
    { 
      field: 'Actions', 
      headerName: 'Actions', 
      width: 130, 
      sortable: false, 
      filter: false, 
      cellRenderer: UserMobileActionsComponent, 
      cellRendererParams: { 
        onDownloadClick: (d: any) => this.onDownloadClick(d), 
        onViewClick: (d: any) => this.onViewClick(d) 
      }, 
      cellClass: 'text-left' 
    }
  ];

  constructor(
    private employeeSalaryService: EmployeeSalaryService,
    private accountService: AccountService,
    private loader: LoaderService,
    private toster: ToastrService,
    private userService: UserService,
    private router: Router,
    private employeeService: EmployeeService,
    private employeeSalaryStructureService: EmployeeSalaryStructureService,
    private departmentService: DepartmentService,
    private designationService: DesignationService
  ) { }

  ngOnInit(): void {
    this.checkScreenSize();
    this.setupResponsiveColumns();
    window.addEventListener('resize', this.onResize.bind(this));
    this.loadLoggedInUserSalary();
  }

  ngOnDestroy(): void {
    window.removeEventListener('resize', this.onResize.bind(this));
  }

  private loadLoggedInUserSalary(): void {
    this.loader.show();
    const user = this.accountService.getCurrentUser();
    if (!user) { 
      this.loader.hide(); 
      return; 
    }
    this.userService.GetUserByIdAsync(user.id).subscribe({
      next: (employee: any) => this.loadEmployeeSalary(employee.EmployeeId),
      error: () => this.loader.hide()
    });
  }

  loadEmployeeSalary(id: any): void {
    forkJoin({
      employeeSalaries: this.employeeSalaryService.getSalariesByEmployee(id),
      employee: this.employeeService.getEmployeeByIdAsync(id),
      employeeSalaryStructure: this.employeeSalaryStructureService.getSalaryStructureByEmployeeAsync(id),
      departments: this.departmentService.getDepartmentsListAsync(),
      designations: this.designationService.getDesignationsListAsync()
    }).subscribe({
      next: (res) => {
        this.employeeSalaries = this.sortMonthlySalariesByYearDesc(res.employeeSalaries);
        this.employee = res.employee;
        this.employeeSalaryStructure = res.employeeSalaryStructure;
        this.departments = res.departments;
        this.designations = res.designations;
        this.loader.hide();
      },
      error: (err) => { 
        this.toster.error('Error loading employee details', err); 
        this.loader.hide(); 
      }
    });
  }

  @HostListener('window:resize', ['$event'])
  onResize(_event: any): void { 
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
    this.columnDefs = this.isMobile ? [...this.mobileColumnDefs] : [...this.desktopColumnDefs];
    this.gridOptions.domLayout = this.isMobile ? 'autoHeight' : 'normal';
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

  onGridReady(params: GridReadyEvent): void {
    this.gridApi = params.api;
    setTimeout(() => this.gridApi.sizeColumnsToFit(), 300);
  }

  getTotalRowsCount(): number { 
    return this.employeeSalaries.length; 
  }
  
  getActiveEmployeesSalariesCount(): number { 
    return this.employeeSalaries.filter(s => s.IsActive).length; 
  }
  
  getInActiveEmployeesSalariesCount(): number { 
    return this.employeeSalaries.filter(s => !s.IsActive).length; 
  }
  
  getEmployeesCount(): number { 
    return new Set(this.employeeSalaries.map(s => s.EmployeeId)).size; 
  }
  
  openAddSalary(): void { }

  private sortMonthlySalariesByYearDesc(salaries: any[]): any[] {
    return [...salaries].sort((a, b) => 
      b.SalaryYear !== a.SalaryYear ? b.SalaryYear - a.SalaryYear : b.SalaryMonth - a.SalaryMonth
    );
  }

  onDownloadClick(salary: EmployeeSalary): void {
    this.loader.show();
    this.selectedPayslipData = this.buildPayslipVM(salary);
    this.pdfMode = 'download';
    this.showPdfRenderer = true;
  }

  onPdfGenerated(): void {
    this.showPdfRenderer = false;
    this.loader.hide();
    this.selectedPayslipData = null;
  }

  onViewClick(salary: EmployeeSalary): void {
    // Show modal immediately with loader
    this.showPreviewModal = true;
    this.isPreviewLoading = true;
    this.previewImageData = null;
    this.loader.show();
    
    // Prepare data in background
    setTimeout(() => {
      this.selectedPayslipData = this.buildPayslipVM(salary);
      this.pdfMode = 'preview';
      this.showPdfRenderer = true;
    }, 100);
  }

  onPreviewReady(imgData: string): void {
    this.showPdfRenderer = false;
    this.previewImageData = imgData;
    this.isPreviewLoading = false;
    this.loader.hide();
    
    // Force modal to stay open on mobile
    if (this.isMobile) {
      setTimeout(() => {
        this.showPreviewModal = true;
      }, 50);
    }
  }

  closePreviewModal(): void {
    this.showPreviewModal = false;
    this.previewImageData = null;
    this.selectedPayslipData = null;
    this.isPreviewLoading = false;
    this.loader.hide();
  }

  printPayslip(): void {
    if (!this.previewImageData) return;
    const win = window.open('', '_blank');
    if (!win) return;
    win.document.write(`<!DOCTYPE html><html><head><title>Payslip</title><style>*{margin:0;padding:0;box-sizing:border-box;}body{background:white;}img{width:100%;display:block;}@media print{body{margin:0;}}</style></head><body><img src="${this.previewImageData}" onload="window.print();window.close();" /></body></html>`);
    win.document.close();
  }

  downloadFromPreview(): void {
    if (!this.selectedPayslipData) return;
    this.closePreviewModal();
    setTimeout(() => {
      this.pdfMode = 'download';
      this.showPdfRenderer = true;
      this.loader.show();
    }, 100);
  }

  private buildPayslipVM(salary: EmployeeSalary): PayslipVM {
    return {
      employeeSalary: salary,
      employee: this.employee ?? undefined,
      employeeSalaryStructure: this.employeeSalaryStructure ?? undefined,
      designation: this.getEmployeeDesignation(this.employee) ?? undefined,
      department: this.getEmployeeDepartment(this.employee) ?? undefined
    };
  }

  getEmployeeDesignation(employee: Employee | null): Designation | null {
    if (!employee) return null;
    return this.designations.find(d => d.DesignationId === employee.DesignationId) ?? null;
  }

  getEmployeeDepartment(employee: Employee | null): Department | null {
    if (!employee) return null;
    return this.departments.find(d => d.DepartmentId === employee.DepartmentId) ?? null;
  }

  employeeInfoRenderer(params: any): string {
    const employeeId = params.data?.EmployeeId;
    if (!employeeId) return '<span class="text-gray-400">-</span>';
    const employee = this.employees.find(e => e.EmployeeId === employeeId);
    if (!employee) return '<span class="text-gray-400">Unknown</span>';
    const displayName = `(${employee.EmployeeCode}) ${employee.FirstName} ${employee.LastName}`.trim();
    return `<span class="employee-link" data-employee-id="${employeeId}" style="text-decoration:none;color:#2196F3;cursor:pointer;">${displayName}</span>`;
  }

  employeeComparator(_va: any, _vb: any, nodeA: any, nodeB: any): number {
    const eA = this.employees.find(e => e.EmployeeId === nodeA.data?.EmployeeId);
    const eB = this.employees.find(e => e.EmployeeId === nodeB.data?.EmployeeId);
    const nA = eA ? `(${eA.EmployeeCode}) ${eA.FirstName} ${eA.LastName}`.trim() : '';
    const nB = eB ? `(${eB.EmployeeCode}) ${eB.FirstName} ${eB.LastName}`.trim() : '';
    return nA.localeCompare(nB);
  }
}
