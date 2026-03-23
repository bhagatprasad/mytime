import { Component, HostListener, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AgGridAngular } from 'ag-grid-angular';
import { AllCommunityModule, ColDef, GridApi, GridOptions, GridReadyEvent, ModuleRegistry } from 'ag-grid-community';
import { ToastrService } from 'ngx-toastr';

import { AttendenceService } from '../../../admin/services/attendence.service';
import { Attendence } from '../../../admin/models/attendence';

ModuleRegistry.registerModules([AllCommunityModule]);

@Component({
  selector: 'app-attendence',
  standalone: true,
  imports: [CommonModule, AgGridAngular],
  templateUrl: './attendence.component.html',
  styleUrl: './attendence.component.css'
})
export class AttendenceComponent implements OnInit, OnDestroy {

  today = new Date().toISOString().split('T')[0];
  attendenceList: Attendence[] = [];
  isMobile: boolean = false;

  private gridApi!: GridApi;
  columnDefs: ColDef[] = [];

  defaultColDef: ColDef = {
    flex: 1,
    minWidth: 120,
    filter: true,
    sortable: true,
    resizable: true
  };

  gridOptions: GridOptions = {
    pagination: true,
    paginationPageSize: 10,
    rowSelection: 'single',
    animateRows: true,
    domLayout: 'autoHeight'
  };

  // 🖥️ Desktop Columns
  desktopColumnDefs: ColDef[] = [
    { field: 'EmployeeId', headerName: 'Employee', width: 150 },
    { field: 'AttendenceDate', headerName: 'Date', width: 150 },
    { field: 'CheckInTime', headerName: 'Check In', width: 150 },
    { field: 'CheckOutTime', headerName: 'Check Out', width: 150 },
    { field: 'WorkHours', headerName: 'Hours', width: 120 },
    { 
      field: 'Status', 
      headerName: 'Status', 
      width: 120,
      cellRenderer: (params: any) => {
        const status = params.value;
        const color = status === 'Present' ? '#2ecc71' : '#e74c3c';
        return `<span style="color:${color};font-weight:600">${status}</span>`;
      }
    },
    { field: 'ApprovalStatus', headerName: 'Approval', width: 140 },
    { field: 'Description', headerName: 'Description', width: 200 }
  ];

  // 📱 Mobile Columns
  mobileColumnDefs: ColDef[] = [
    { field: 'AttendenceDate', headerName: 'Date', width: 120 },
    { 
      field: 'Status', 
      headerName: 'Status', 
      width: 120,
      cellRenderer: (params: any) => {
        return `<span>${params.value}</span>`;
      }
    },
    { field: 'WorkHours', headerName: 'Hours', width: 100 }
  ];

  constructor(
    private attendenceService: AttendenceService,
    private toastr: ToastrService
  ) {}

  ngOnInit(): void {
    this.checkScreenSize();
    this.setupResponsiveColumns();
    window.addEventListener('resize', this.onResize.bind(this));
    this.loadAttendence();
  }

  ngOnDestroy(): void {
    window.removeEventListener('resize', this.onResize.bind(this));
  }

  // 📊 Load Data
  loadAttendence(): void {
    this.attendenceService.getAttendenceListAsync().subscribe({
      next: (res) => {
        this.attendenceList = res;
      },
      error: () => {
        this.toastr.error('Error loading attendence');
      }
    });
  }
  checkIn() {
  const payload = {
    employeeId: this.employeeId,
    attendenceDate: new Date().toISOString().split('T')[0],
    checkInTime: new Date().toISOString()
  };

  this.attendenceService.checkIn(payload).subscribe({
    next: (res: any) => {
      console.log('Check-in successful', res);
      alert('Checked in successfully');
      this.loadAttendence(); // refresh list
    },
    error: (err: any) => {
      console.error(err);
      alert('Check-in failed');
    }
  });
}

  // 📱 Responsive
 @HostListener('window:resize', ['$event'])
  onResize(event: Event): void {
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
    this.columnDefs = this.isMobile
      ? [...this.mobileColumnDefs]
      : [...this.desktopColumnDefs];

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

  // 📊 Dashboard Counts
  getTotal(): number {
    return this.attendenceList.length;
  }

  getPresent(): number {
    return this.attendenceList.filter(x => x.Status === 'Present').length;
  }

  getAbsent(): number {
    return this.attendenceList.filter(x => x.Status === 'Absent').length;
  }

  getPending(): number {
    return this.attendenceList.filter(x => x.ApprovalStatus === 'Pending').length;
  }
}