import { CommonModule, DatePipe } from '@angular/common';
import { Component, HostListener, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { OnIdentifyEffects } from '@ngrx/effects';
import { AgGridAngular } from 'ag-grid-angular';
import { AllCommunityModule, ColDef, GridApi, GridOptions, GridReadyEvent, ICellRendererParams, ModuleRegistry, ValueFormatterParams } from 'ag-grid-community';
import { ActionsRendererComponent } from '../../../common/components/actions-renderer.component';
import { MobileActionsRendererComponent } from '../../../common/components/mobile-actions-renderer.component';
import { LeaveRequest } from '../../models/leave-request.model';
import { ToastrService } from 'ngx-toastr';
import { LoaderService } from '../../../common/services/loader.service';
import { AuditFieldsService } from '../../../common/services/auditfields.service';
import { LeaveService } from '../../services/leave.service';
import { Designation } from '../../models/designation';
import { Employee } from '../../models/employee';
import { User } from '../../models/user';
import { EmployeeService } from '../../services/employee.service';
import { LeaveType } from '../../models/leave-type.model';

ModuleRegistry.registerModules([AllCommunityModule]);

@Component({
  selector: 'app-apply-leave',
  standalone: true,
  imports: [CommonModule, AgGridAngular, DatePipe, FormsModule],
  templateUrl: './apply-leave.component.html',
  styleUrl: './apply-leave.component.css'
})
export class ApplyLeaveComponent implements OnInit {

  today = new Date();
  // Grid API
  private gridApi!: GridApi;

  // Responsive state
  isMobile: boolean = false;
  leaveTypes: LeaveType[] = [];

  showPopup = false;
  selectedRow: any;
  actionType = '';
  adminComment = '';

  // Desktop Columns (7-8 columns)
  desktopColumnDefs: ColDef[] = [
    {
      field: 'Id',
      headerName: 'ID',
      width: 80,
      filter: 'agNumberColumnFilter',
      sortable: true,
      cellClass: 'text-center',
    },
    {
      field: 'UserId',
      headerName: 'Employee',
      width: 180,
      sortable: true,
      filter: 'agTextColumnFilter',

      valueGetter: (params: any) => {

        const emp = this.employees.find(
          e => Number(e.UserId) === Number(params.data.UserId)
        );

        if (!emp) return params.data.UserId;

        const firstName = this.capitalize(emp.FirstName);
        const lastName = this.capitalize(emp.LastName);

        return `${firstName} ${lastName}`.trim();
      }
    },
    {
      field: 'LeaveTypeId',
      headerName: 'Leave Type',
      width: 160,
      sortable: true,
      filter: 'agTextColumnFilter',
      cellClass: 'text-center',

      valueGetter: (params: any) => {

        const type = this.leaveTypes.find(
          t => Number(t.Id) === Number(params.data.LeaveTypeId)
        );

        return type ? type.Name : params.data.LeaveTypeId;

      }
    },
    {
      field: 'Reason',
      headerName: 'Reason',
      width: 120,
      filter: 'agTextColumnFilter',
      sortable: true,
      cellClass: 'text-center'
    },
    {
      field: 'Description',
      headerName: 'Description',
      width: 120,
      filter: 'agTextColumnFilter',
      sortable: true,
      cellClass: 'text-center'
    },
    {
      field: 'FromDate',
      headerName: 'FromDate',
      width: 120,
      filter: 'agTextColumnFilter',
      sortable: true,
      cellClass: 'text-center'
    },
    {
      field: 'ToDate',
      headerName: 'ToDate',
      width: 120,
      filter: 'agTextColumnFilter',
      sortable: true,
      cellClass: 'text-center'
    },
    {
      field: 'TotalDays',
      headerName: 'TotalDays',
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
      field: 'Status',
      headerName: 'Status',
      width: 120,
      sortable: true,
      filter: 'agTextColumnFilter',
      cellClass: 'text-left',
      cellRenderer: (params: any) => {

        const status = (params.value || '').toLowerCase();

        return `<span class="status-pill status-${status}">
              ${params.value}
            </span>`;
      }
    },
    {
      headerName: 'Actions',
      field: 'actions',
      width: 120,
      cellRenderer: (params: any) => {

        const disabled = params.data.Status === 'Cancelled' ? 'disabled' : '';

        return `
      <div class="action-icons">

        <button class="icon-btn approve-btn"
          title="Approve Leave"
          ${disabled}>
          <i class="mdi mdi-check-circle"></i>
        </button>

        <button class="icon-btn reject-btn"
          title="Reject Leave"
          ${disabled}>
          <i class="mdi mdi-close-circle"></i>
        </button>

      </div>
    `;
      }
    }
  ];

  mobileColumnDefs: ColDef[] = [
    {
      field: 'UserId',
      headerName: 'Employee',
      width: 180,
      sortable: true,
      filter: 'agTextColumnFilter',

      valueGetter: (params: any) => {

        const emp = this.employees.find(
          e => Number(e.UserId) === Number(params.data.UserId)
        );

        if (!emp) return params.data.UserId;

        const firstName = this.capitalize(emp.FirstName);
        const lastName = this.capitalize(emp.LastName);

        return `${firstName} ${lastName}`.trim();
      }
    },
    {
      field: 'Reason',
      headerName: 'Reason',
      width: 100,
      cellClass: 'text-center'
    },
    {
      headerName: 'Actions',
      field: 'actions',
      width: 120,
      cellRenderer: (params: any) => {

        const disabled = params.data.Status === 'Cancelled' ? 'disabled' : '';

        return `
      <div class="action-icons">

        <button class="icon-btn approve-btn"
          title="Approve Leave"
          ${disabled}>
          <i class="mdi mdi-check-circle"></i>
        </button>

        <button class="icon-btn reject-btn"
          title="Reject Leave"
          ${disabled}>
          <i class="mdi mdi-close-circle"></i>
        </button>

      </div>
    `;
      }
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

  rowData: LeaveRequest[] = [];
  employees: Employee[] = [];

  constructor(
    // private designationService: DesignationService,
    private toastr: ToastrService,
    private loader: LoaderService,
    private audit: AuditFieldsService,
    private leaveService: LeaveService,
    private employeeService: EmployeeService,
  ) { }

  ngOnInit(): void {
    this.checkScreenSize();
    this.setupResponsiveColumns();
    this.loadleaveData();
    this.loadEmployees();
    this.getLeaveTypes();
    window.addEventListener('resize', this.onResize.bind(this));
  }

  ngOnDestroy(): void {
    window.removeEventListener('resize', this.onResize.bind(this));
  }

  @HostListener('window:resize', ['$event'])
  onResize(event: any): void {
    this.checkScreenSize();
  }

  capitalize(name?: string | null): string {
    if (!name) return '';
    return name.charAt(0).toUpperCase() + name.slice(1).toLowerCase();
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

  loadleaveData(): void {
    this.loader.show();

    this.leaveService.GetAllleaveRequestsAsync().subscribe({
      next: (des: LeaveRequest[]) => {
        this.rowData = des;
        this.loader.hide();
        if (this.gridApi) {
          setTimeout(() => {
            this.gridApi.sizeColumnsToFit();
          }, 100);
        }
      },
      error: (error) => {
        console.error('Error loading designations:', error);
        this.loader.hide();

        this.toastr.error('Failed to load designations.', 'Error');
      }
    });
  }

  onGridReady(params: GridReadyEvent): void {
    this.gridApi = params.api;
    setTimeout(() => {
      this.gridApi.sizeColumnsToFit();
    }, 300);
  }

  openCommentPopup(row: any, action: string) {

    this.selectedRow = row;
    this.actionType = action;
    this.showPopup = true;

  }

  onCellClicked(event: any) {

    const target = event.event.target;

    const approveBtn = target.closest('.approve-btn');
    const rejectBtn = target.closest('.reject-btn');

    if (approveBtn) {
      this.openCommentPopup(event.data, 'approve');
    }

    if (rejectBtn) {
      this.openCommentPopup(event.data, 'reject');
    }

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
    this.loadleaveData();
  }

  closePopup() {
    this.showPopup = false;
    this.adminComment = '';
  }

  loadEmployees() {
    this.employeeService.getEmployeesListAsync().subscribe(res => {
      this.employees = res;
      if (this.gridApi) {
        this.gridApi.refreshCells();
      }
    });
  }

  getLeaveTypes() {
  this.leaveService.GetleaveTypesAsync().subscribe(res => {

    this.leaveTypes = res;

    if (this.gridApi) {
      this.gridApi.refreshCells();
    }

  });
}

  submitAction() {

    const id = this.selectedRow.Id;

    const payload = {
      adminComment: this.adminComment
    };

    if (this.actionType === 'reject') {

      this.leaveService.RejectLeaveAsync(id, payload).subscribe(res => {
        this.closePopup()
        this.refreshData(); // reload grid;

      });

    }

    if (this.actionType === 'approve') {

      this.leaveService.ApproveLeaveAsync(id, payload).subscribe(res => {
        this.closePopup();
        this.refreshData();

      });
    }
  }

  getSelectedRowsCount(): number {
    return this.gridApi?.getSelectedRows()?.length || 0;
  }

  getTotalRowsCount(): number {
    return this.rowData.length;
  }

  getActiveRolesCount(): number {
    return this.rowData.filter(des => des.IsActive).length;
  }

  getInactiveRolesCount(): number {
    return this.rowData.filter(des => !des.IsActive).length;
  }
}
