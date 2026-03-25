import { Component, HostListener, OnInit, OnDestroy } from '@angular/core';
import { LoaderService } from '../../../common/services/loader.service';
import { CommonModule } from '@angular/common';
import { AccountService } from '../../../common/services/account.service';
import { AllCommunityModule, ColDef, GridApi, GridOptions, GridReadyEvent, ModuleRegistry } from 'ag-grid-community';
import { ToastrService } from 'ngx-toastr';
import { AgGridAngular, } from 'ag-grid-angular';
import { RouterModule } from '@angular/router';
import { CreateAttendance } from './create-attendance';
import { AuditFieldsService } from '../../../common/services/auditfields.service';
import { UserActionComponent } from '../common/user-action-component';
import { Attendence } from '../../../admin/models/attendence';
import { AttendenceService } from '../../../admin/services/attendence.service';

ModuleRegistry.registerModules([AllCommunityModule]);

@Component({
  selector: 'app-attendence',
  standalone: true,
  imports: [CommonModule, AgGridAngular, RouterModule, CreateAttendance],
  templateUrl: './attendence.component.html',
  styleUrl: './attendence.component.css'
})
export class AttendenceComponent implements OnInit, OnDestroy {

  employeeId: any = 0;
  isMobile: boolean = false;
  private gridApi!: GridApi;
  columnDefs: ColDef[] = [];

  employeeAttendence: Attendence[] = [];
  selectedAttendence: Attendence | null = null;
  showAttendenceView: boolean = false;
  selectedAttendenceId: number | null = null;

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
    { field: 'AttendenceDate', headerName: 'Date', width: 140, filter: 'agTextColumnFilter', sortable: true, cellClass: 'text-center', valueGetter: (p) => p.data.AttendenceDate ? new Date(p.data.AttendenceDate).toLocaleDateString('en-IN') : '' },
    { field: 'WorkType', headerName: 'Work Type', width: 130, filter: 'agTextColumnFilter', sortable: true, cellClass: 'text-center' },
    { field: 'CheckInTime', headerName: 'Check-In', width: 180, filter: 'agTextColumnFilter', sortable: true, cellClass: 'text-center', valueGetter: (p) => `${p.data.CheckInTime} / ${p.data.CheckOutTime}` },
    { field: 'CheckOutTime', headerName: 'Check-Out', width: 180, filter: 'agTextColumnFilter', sortable: true, cellClass: 'text-center', valueGetter: (p) => `${p.data.CheckInTime} / ${p.data.CheckOutTime}` },
    { field: 'WorkHours', headerName: 'Work Hours', width: 130, filter: 'agTextColumnFilter', sortable: true, cellClass: 'text-center', valueGetter: (p) => p.data.WorkHours != null ? `${p.data.WorkHours}h` : '0h' },
    { field: 'Description', headerName: 'Description', width: 200, filter: 'agTextColumnFilter', sortable: false, cellClass: 'text-left' },
    { field: 'Status', headerName: 'Status', width: 120, filter: 'agTextColumnFilter', sortable: true, cellClass: 'text-center' },
    { field: 'Actions', headerName: 'Actions', width: 160, sortable: false, filter: false, cellRenderer: UserActionComponent, cellRendererParams: { onViewClick: (d: any) => this.onViewClick(d), onEditClick: (d: any) => this.openEditForm(d) }, cellClass: 'text-left' }
  ];
  mobileColumnDefs: ColDef[] = [
    { field: 'AttendenceDate', headerName: 'Date', flex: 1, cellClass: 'text-center', valueGetter: (p) => p.data.AttendenceDate ? new Date(p.data.AttendenceDate).toLocaleDateString('en-IN') : '' },
    { field: 'CheckInTime', headerName: 'In/Out', flex: 1.2, cellClass: 'text-center', valueGetter: (p) => `${p.data.CheckInTime} / ${p.data.CheckOutTime}` },
    { field: 'WorkHours', headerName: 'Hours', flex: 1, cellClass: 'text-center', valueGetter: (p) => p.data.WorkHours != null ? `${p.data.WorkHours}h` : '0h' },
    { field: 'Actions', headerName: '', flex: 0.8, sortable: false, filter: false, cellRenderer: UserActionComponent, cellRendererParams: { onViewClick: (d: any) => this.onViewClick(d), onEditClick: (d: any) => this.openEditForm(d) }, cellClass: 'text-left' }

  ];
  constructor(
    private accountService: AccountService,
    private attendenceService: AttendenceService,
    private loader: LoaderService,
    private toster: ToastrService,
    private audit: AuditFieldsService,
  ) { }
  ngOnInit(): void {
    this.checkScreenSize();
    this.setupResponsiveColumns();
    window.addEventListener('resize', this.onResize.bind(this));
    this.loadAttendence();
  }

  ngOnDestroy(): void {
    window.removeEventListener('resize', this.onResize.bind(this));
  }

  private loadAttendence(): void {
    this.loader.show();
    const user = this.accountService.getCurrentUser();
    if (!user) {
      this.loader.hide();
      return;
    }
    this.employeeId = user.employeeId;
    this.loadEmployeeAttendence(user.employeeId);
  }

  loadEmployeeAttendence(employeeId: any): void {
    this.attendenceService.getAttendenceListByEmployeeAsync(employeeId).subscribe({
      next: (res: any) => {
        this.employeeAttendence = res;
        this.loader.hide();
      },
      error: (err) => {
        this.toster.error('Error loading employee details', err);
        this.loader.hide();
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
    const newColumnDefs = JSON.parse(JSON.stringify(this.columnDefs));
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
    return this.employeeAttendence ? this.employeeAttendence.length : 0;
  }


  onViewClick(attendence: Attendence): void {
    this.selectedAttendence = attendence;   // selected data store
    this.showAttendenceView = true;         // view popup open

    console.log('View attendence:', attendence);
  }
  openEditForm(data: any): void {

  }
  getAttendenceCount(): number {
    return new Set(this.employeeAttendence.map(s => s.EmployeeId)).size;
  }
  openAddAttendenceSideBar(): void {
    this.showAttendenceView = true;
    this.selectedAttendence = null;
  }
  onSaveAttendance(att: Attendence): void {
    this.loader.show();

    const _att = this.audit.appendAuditFields(att);

    console.log("Received attendance data:", _att);
    this.attendenceService.insertOrUpdateAttendence(_att).subscribe(
      response => {
        this.loader.hide();

        if (response) {
          this.toster.success("Attendance processed successfully");
          this.showAttendenceView = false;   // close sidebar after save
          this.refreshData();
        }
      },
      error => {
        this.loader.hide();
        console.error(error);
        this.toster.error("Something went wrong, please check and resubmit");
        this.showAttendenceView = true;
      }
    );
  }
  refreshData(): void {
    this.loadAttendence();
  }

}