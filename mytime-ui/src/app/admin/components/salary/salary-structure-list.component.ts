import { CommonModule } from '@angular/common';
import { Component, HostListener, OnDestroy, OnInit } from '@angular/core';
import { AgGridAngular } from 'ag-grid-angular';
import { AllCommunityModule, ColDef, GridApi, GridOptions, GridReadyEvent, ICellRendererParams, ModuleRegistry } from 'ag-grid-community';
import { EmployeeSalaryStructure } from '../../models/employee_salary_structure';
import { Employee } from '../../models/employee';
import { Router } from '@angular/router';
import { EmployeeSalaryStructureService } from '../../services/employee_salary_structure.service';
import { EmployeeService } from '../../services/employee.service';
import { LoaderService } from '../../../common/services/loader.service';
import { ToastrService } from 'ngx-toastr';
import { AuditFieldsService } from '../../../common/services/auditfields.service';
import { forkJoin } from 'rxjs';

ModuleRegistry.registerModules([AllCommunityModule]);

@Component({
  selector: 'app-salary-structure-list',
  standalone: true,
  imports: [CommonModule, AgGridAngular],
  templateUrl: './salary-structure-list.component.html',
  styleUrl: './salary-structure-list.component.css'
})
export class SalaryStructureListComponent implements OnInit, OnDestroy {

  today = new Date();

  private gridApi!: GridApi;

  isMobile: boolean = false;

  columnDefs: ColDef[] = [];

  employeeSalaryStructures: EmployeeSalaryStructure[] = [];

  employees: Employee[] = [];

  selectedEmployeeSalaryStructure: EmployeeSalaryStructure | null = null;

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
    width: 180,
    minWidth: 180,
    sortable: true,
    filter: 'agTextColumnFilter',
    cellRenderer: this.employeeInfoRenderer.bind(this),
    comparator: this.employeeComparator.bind(this),
    cellClass: 'text-left',
    onCellClicked: (params: any) => {
      if (params.data?.EmployeeId) {
        this.router.navigate(['/admin/employees', params.data.EmployeeId]);
      }
    }
  },
  {
    headerName: 'Identity & Bank',
    width: 280,
    minWidth: 250,
    sortable: false,
    filter: false,
    cellRenderer: (params: any) => {
      const data = params.data;
      return `
        <div class="d-flex flex-column" style="line-height: 1.4;">
          <div class="d-flex align-items-center gap-2 mb-1">
            <span class="badge bg-light text-dark px-2">PAN</span>
            <span class="fw-medium">${data.PAN || '—'}</span>
          </div>
          <div class="d-flex align-items-center gap-2 mb-1">
            <span class="badge bg-light text-dark px-2">Aadhaar</span>
            <span class="fw-medium">${data.Adhar || '—'}</span>
          </div>
          <div class="d-flex align-items-center gap-2">
            <span class="badge bg-light text-dark px-2">Bank</span>
            <span class="fw-medium">${data.BankName || '—'}</span>
            <span class="text-muted small">${data.BankAccount ? '****' + data.BankAccount.slice(-4) : '—'}</span>
          </div>
          <div class="small text-muted mt-1">
            IFSC: ${data.IFSC || '—'} | UAN: ${data.UAN || '—'}
          </div>
        </div>
      `;
    },
    cellClass: 'identity-bank-cell',
    tooltipField: 'PAN'
  },
  {
    headerName: 'Earnings (₹)',
    width: 280,
    minWidth: 250,
    sortable: true,
    filter: 'agNumberColumnFilter',
    comparator: (valueA: any, valueB: any, nodeA: any, nodeB: any) => {
      return (nodeA.data?.GROSSEARNINGS || 0) - (nodeB.data?.GROSSEARNINGS || 0);
    },
    cellRenderer: (params: any) => {
      const data = params.data;
      const totalEarnings = data.GROSSEARNINGS || 0;
      
      return `
        <div class="d-flex flex-column earnings-cell" style="line-height: 1.4;">
          <div class="d-flex justify-content-between align-items-center mb-1">
            <span class="text-muted small">Basic + HRA:</span>
            <span class="fw-medium">${this.formatRupeesCompact((data.BASIC || 0) + (data.HRA || 0))}</span>
          </div>
          <div class="d-flex justify-content-between align-items-center mb-1">
            <span class="text-muted small">Allowances:</span>
            <span class="fw-medium">${this.formatRupeesCompact((data.CONVEYANCE || 0) + (data.MEDICALALLOWANCE || 0) + (data.SPECIALALLOWANCE || 0))}</span>
          </div>
          <div class="d-flex justify-content-between align-items-center mb-1">
            <span class="text-muted small">Bonus/Others:</span>
            <span class="fw-medium">${this.formatRupeesCompact((data.SPECIALBONUS || 0) + (data.STATUTORYBONUS || 0) + (data.OTHERS || 0))}</span>
          </div>
          <div class="d-flex justify-content-between align-items-center pt-1 border-top">
            <span class="fw-semibold">Total:</span>
            <span class="fw-bold text-primary">${this.formatRupees(totalEarnings)}</span>
          </div>
        </div>
      `;
    },
    cellClass: 'earnings-cell',
    tooltipValueGetter: (params: any) => {
      const data = params.data;
      return `Basic: ${this.formatRupeesCompact(data.BASIC)} | HRA: ${this.formatRupeesCompact(data.HRA)} | Conveyance: ${this.formatRupeesCompact(data.CONVEYANCE)} | Medical: ${this.formatRupeesCompact(data.MEDICALALLOWANCE)} | Special: ${this.formatRupeesCompact(data.SPECIALALLOWANCE)} | Bonus: ${this.formatRupeesCompact(data.SPECIALBONUS)} | Statutory: ${this.formatRupeesCompact(data.STATUTORYBONUS)} | Others: ${this.formatRupeesCompact(data.OTHERS)}`;
    }
  },
  {
    headerName: 'Deductions (₹)',
    width: 260,
    minWidth: 230,
    sortable: true,
    filter: 'agNumberColumnFilter',
    comparator: (valueA: any, valueB: any, nodeA: any, nodeB: any) => {
      return (nodeA.data?.GROSSDEDUCTIONS || 0) - (nodeB.data?.GROSSDEDUCTIONS || 0);
    },
    cellRenderer: (params: any) => {
      const data = params.data;
      const totalDeductions = data.GROSSDEDUCTIONS || 0;
      
      return `
        <div class="d-flex flex-column deductions-cell" style="line-height: 1.4;">
          <div class="d-flex justify-content-between align-items-center mb-1">
            <span class="text-muted small">PF + ESIC:</span>
            <span class="fw-medium">${this.formatRupeesCompact((data.PF || 0) + (data.ESIC || 0))}</span>
          </div>
          <div class="d-flex justify-content-between align-items-center mb-1">
            <span class="text-muted small">Professional Tax:</span>
            <span class="fw-medium">${this.formatRupeesCompact(data.PROFESSIONALTAX || 0)}</span>
          </div>
          <div class="d-flex justify-content-between align-items-center mb-1">
            <span class="text-muted small">Health Insurance:</span>
            <span class="fw-medium">${this.formatRupeesCompact(data.GroupHealthInsurance || 0)}</span>
          </div>
          <div class="d-flex justify-content-between align-items-center pt-1 border-top">
            <span class="fw-semibold">Total:</span>
            <span class="fw-bold text-danger">${this.formatRupees(totalDeductions)}</span>
          </div>
        </div>
      `;
    },
    cellClass: 'deductions-cell',
    tooltipValueGetter: (params: any) => {
      const data = params.data;
      return `PF: ${this.formatRupeesCompact(data.PF)} | ESIC: ${this.formatRupeesCompact(data.ESIC)} | Professional Tax: ${this.formatRupeesCompact(data.PROFESSIONALTAX)} | Health Insurance: ${this.formatRupeesCompact(data.GroupHealthInsurance)}`;
    }
  },
  {
    headerName: 'Net & Status',
    width: 200,
    minWidth: 180,
    sortable: true,
    filter: false,
    cellRenderer: (params: any) => {
      const data = params.data;
      const netSalary = this.calculateNetSalary(data);
      const isActive = data.IsActive;
      const statusClass = isActive ? 'success' : 'danger';
      const statusText = isActive ? 'Active' : 'Inactive';
      
      return `
        <div class="d-flex flex-column net-status-cell" style="line-height: 1.4;">
          <div class="d-flex justify-content-between align-items-center mb-2">
            <span class="text-muted small">Net Salary:</span>
            <span class="fw-bold" style="color: #10b981;">${this.formatRupees(netSalary)}</span>
          </div>
          <div class="d-flex align-items-center justify-content-between">
            <span class="text-muted small">Status:</span>
            <span class="badge bg-${statusClass}">${statusText}</span>
          </div>
          <div class="d-flex gap-2 mt-2">
            <button class="btn btn-xs btn-outline-primary py-0 px-2" onclick="window.editSalaryStructure(${data.EmployeeId})" title="Edit">
              <i class="mdi mdi-pencil" style="font-size: 14px;"></i>
            </button>
            <button class="btn btn-xs btn-outline-danger py-0 px-2" onclick="window.deleteSalaryStructure(${data.EmployeeId})" title="Delete">
              <i class="mdi mdi-delete" style="font-size: 14px;"></i>
            </button>
          </div>
        </div>
      `;
    },
    cellClass: 'net-status-cell',
    comparator: (valueA: any, valueB: any, nodeA: any, nodeB: any) => {
      const netA = this.calculateNetSalary(nodeA.data);
      const netB = this.calculateNetSalary(nodeB.data);
      return netA - netB;
    }
  }
];

  mobileColumnDefs: ColDef[] = [
    {
      headerName: 'Employee',
      width: 180,
      sortable: true,
      filter: 'agTextColumnFilter',
      cellRenderer: this.employeeInfoRenderer.bind(this),
      comparator: this.employeeComparator.bind(this),
      cellClass: 'text-left',
      onCellClicked: (params: any) => {
        if (params.data?.EmployeeId) {
          this.router.navigate(['/admin/employees', params.data.EmployeeId]);
        }
      }
    },
    {
      headerName: 'Earnings',
      width: 180,
      sortable: true,
      filter: 'agNumberColumnFilter',
      cellClass: 'text-left',
      cellRenderer: (params: any): string => {
        const basic = params.data?.BASIC ?? 0;
        const hra = params.data?.HRA ?? 0;
        const gross = params.data?.GROSSEARNINGS ?? 0;

        const fmt = (val: number) =>
          `₹${Number(val).toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;

        return `
        <div style="line-height: 1.5; padding: 2px 0;">
          <div style="font-size: 12px; color: #666;">
            Basic: <span style="color: #2196F3; font-weight: 500;">${fmt(basic)}</span>
            &nbsp;|&nbsp;
            HRA: <span style="color: #2196F3; font-weight: 500;">${fmt(hra)}</span>
          </div>
          <div style="font-size: 13px; font-weight: 600; color: #2196F3;">
            Gross: ${fmt(gross)}
          </div>
        </div>`;
      },
      valueGetter: (params) => params.data?.GROSSEARNINGS ?? 0
    },
    {
      headerName: 'Deductions',
      width: 180,
      sortable: true,
      filter: 'agNumberColumnFilter',
      cellClass: 'text-left',
      cellRenderer: (params: any): string => {
        const pf = params.data?.PF ?? 0;
        const esic = params.data?.ESIC ?? 0;
        const grossDed = params.data?.GROSSDEDUCTIONS ?? 0;

        const fmt = (val: number) =>
          `₹${Number(val).toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;

        return `
        <div style="line-height: 1.5; padding: 2px 0;">
          <div style="font-size: 12px; color: #666;">
            PF: <span style="color: #f44336; font-weight: 500;">${fmt(pf)}</span>
            &nbsp;|&nbsp;
            ESIC: <span style="color: #f44336; font-weight: 500;">${fmt(esic)}</span>
          </div>
          <div style="font-size: 13px; font-weight: 600; color: #f44336;">
            Total: ${fmt(grossDed)}
          </div>
        </div>`;
      },
      valueGetter: (params) => params.data?.GROSSDEDUCTIONS ?? 0
    },
    {
      headerName: 'Bank Info',
      width: 180,
      sortable: false,
      filter: 'agTextColumnFilter',
      cellClass: 'text-left',
      cellRenderer: (params: any): string => {
        const bank = params.data?.BankName || '—';
        const account = params.data?.BankAccount || '—';
        const ifsc = params.data?.IFSC || '—';

        return `
        <div style="line-height: 1.5; padding: 2px 0;">
          <div style="font-size: 13px; font-weight: 500; color: #333;">${bank}</div>
          <div style="font-size: 11px; color: #666;">
            Acc: ${account}
          </div>
          <div style="font-size: 11px; color: #888;">
            IFSC: ${ifsc}
          </div>
        </div>`;
      },
      valueGetter: (params) => params.data?.BankName ?? ''
    },
    {
      field: 'IsActive',
      headerName: 'Status',
      width: 90,
      sortable: true,
      filter: 'agTextColumnFilter',
      cellClass: 'text-center',
      cellRenderer: this.mobileStatusRenderer.bind(this)
    }
  ];

  constructor(
    private salaryStructureService: EmployeeSalaryStructureService,
    private employeeService: EmployeeService,
    private loader: LoaderService,
    private toastr: ToastrService,
    private audit: AuditFieldsService,
    private router: Router) { }

  ngOnDestroy(): void {
    window.removeEventListener('resize', this.onResize.bind(this));
  }
  ngOnInit(): void {
    this.checkScreenSize();
    this.setupResponsiveColumns();
    window.addEventListener('resize', this.onResize.bind(this));
    this.loadInitialData();
  }
  loadInitialData(): void {
    this.loader.show();

    forkJoin({
      salaryStructures: this.salaryStructureService.getEmployeeSalaryStructureListAsync(),
      employees: this.employeeService.getEmployeesListAsync()
    }).subscribe({
      next: ({ salaryStructures, employees }) => {
        this.employeeSalaryStructures = salaryStructures;
        this.employees = employees;
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
        this.toastr.error('Failed to load data');
      }
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

  mobileStatusRenderer(params: ICellRendererParams): string {
    const isActive = params.value;
    const statusText = isActive ? 'Active' : 'Inactive';
    const statusClass = isActive ? 'success' : 'danger';

    return `<span class="badge bg-${statusClass}">${statusText}</span>`;
  }
  openAddSalaryStructure(): void {

  }
  getTotalRowsCount(): number {
    return 0;
  }

  getEmployeesCount(): number {
    return 0;
  }
  rupeesFormatter(params: any): string {
    if (params.value == null || params.value === '') return '—';
    const formatted = Number(params.value).toLocaleString('en-IN', {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    });
    return `₹${formatted}`;
  }

  getRupeesCellStyle(): any {
    return { color: '#2196F3', fontWeight: '500' };
  }

  formatRupees(value: any): string {
    if (value === null || value === undefined || value === '') return '—';


    const numValue = typeof value === 'string' ? parseFloat(value) : value;

    if (isNaN(numValue) || numValue === 0) return '—';

    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    }).format(numValue);
  }

  calculateNetSalary(data: any): number {
    return (data?.GROSSEARNINGS || 0) - (data?.GROSSDEDUCTIONS || 0);
  }

  formatRupeesCompact(value: any): string {
    if (value === null || value === undefined || value === '') return '—';

    const numValue = typeof value === 'string' ? parseFloat(value) : value;

    if (isNaN(numValue) || numValue === 0) return '—';

    // Check if it's a whole number
    if (numValue % 1 === 0) {
      return `₹${numValue.toLocaleString('en-IN')}`;
    }

    return `₹${numValue.toLocaleString('en-IN', {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    })}`;
  }
}