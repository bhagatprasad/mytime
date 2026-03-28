import { CommonModule } from '@angular/common';
import { Component, HostListener, OnDestroy, OnInit } from '@angular/core';
import { Timesheet } from '../../../common/models/timesheet';
import { TimesheetService } from '../../../common/services/timesheet.service';
import {
  AllCommunityModule,
  ColDef,
  GridApi,
  GridOptions,
  GridReadyEvent,
  ModuleRegistry,
  ValueFormatterParams,
} from 'ag-grid-community';
import { AgGridModule } from 'ag-grid-angular';
import { ToastrService } from 'ngx-toastr';
import { LoaderService } from '../../../common/services/loader.service';
import { AddTimesheetComponent } from './add-timesheet.component';

ModuleRegistry.registerModules([AllCommunityModule]);

@Component({
  selector: 'app-list-timesheet',
  standalone: true,
  imports: [CommonModule, AgGridModule, AddTimesheetComponent],
  templateUrl: './list-timesheet.component.html',
  styleUrl: './list-timesheet.component.css',
})
export class ListTimesheetComponent implements OnInit, OnDestroy {
  timesheets: Timesheet[] = [];
  today = new Date();
  private gridApi!: GridApi;
  isMobile: boolean = false;

  showForm: boolean = false;

  constructor(
    private timesheetService: TimesheetService,
    private toastr: ToastrService,
    private loader: LoaderService,
  ) {}

  ngOnInit(): void {
    this.setupResponsiveColumns();
    this.LoadTimesheetDetails();
    this.checkScreenSize();
    window.addEventListener('resize', this.onResize.bind(this));
  }

  ngOnDestroy(): void {
    window.removeEventListener('resize', this.onResize.bind(this));
  }

  @HostListener('window:resize', ['$event'])
  onResize(event: any): void {
    this.checkScreenSize();
  }

  toggleForm() {
    this.showForm = true;
  }

  closeForm() {
    this.showForm = false;
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
    setTimeout(() => {
      this.gridApi.refreshHeader();
      this.gridApi.sizeColumnsToFit();
    }, 100);
  }

  LoadTimesheetDetails(): void {
    this.loader.show();
    this.timesheetService.getTimesheetsListAsync().subscribe({
      next: (timesheet: Timesheet[]) => {
        this.timesheets = timesheet;
        this.loader.hide();

        if (this.gridApi) {
          setTimeout(() => {
            this.gridApi.sizeColumnsToFit();
          }, 100);
        }
      },
      error: (error) => {
        console.log('error fetching timesheet details', error);
        this.loader.hide();
        this.toastr.error('failed to load timesheet', 'Error');
      },
    });
  }

  getTotalRowsCount(): number {
    return this.timesheets.length;
  }

  getActiveTimesheetCount(): number {
    return this.timesheets.filter((timesheet) => timesheet.IsActive).length;
  }

  getInactiveTimesheetCount(): number {
    return this.timesheets.filter((timesheet) => !timesheet.IsActive).length;
  }

  onGridReady(params: GridReadyEvent): void {
    this.gridApi = params.api;
    setTimeout(() => {
      this.gridApi.sizeColumnsToFit();
    }, 300);
  }

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
    paginationPageSizeSelector: [10, 20, 40, 100],
    rowSelection: 'single',
    animateRows: true,
    enableCellTextSelection: true,
    suppressRowClickSelection: false,
    domLayout: 'autoHeight',
  };

  desktopColumnDefs: ColDef[] = [
    {
      headerName: 'Timesheet_Date Range',
      width: 180,
      sortable: true,
      filter: 'agTextColumnFilter',
      cellClass: 'text-left',
      valueGetter: (params) => {
        const from = params.data?.FromDate
          ? new Date(params.data.FromDate).toLocaleDateString('en-GB')
          : '';
        const to = params.data?.ToDate
          ? new Date(params.data.ToDate).toLocaleDateString('en-GB')
          : '';
        return `${from}  -  ${to}`;
      },
    },
    {
      field: 'Description',
      headerName: 'Timesheet_Description',
      width: 120,
      filter: 'agTextColumnFilter',
      sortable: true,
      cellClass: 'text-left',
    },
    {
      field: 'Status',
      headerName: 'Timesheet_Status',
      width: 120,
      filter: 'agTextColumnFilter',
      sortable: true,
      cellClass: 'text-left',
    },
    {
      field: 'TotalHrs',
      headerName: 'Timesheet_TotalHours',
      width: 120,
      filter: 'agNumberColumnFilter',
      sortable: true,
      cellClass: 'text-left',
    },
  ];

  mobileColumnDefs: ColDef[] = [
    {
      headerName: 'Date Range',
      width: 160,
      sortable: true,
      filter: 'agTextColumnFilter',
      cellClass: 'text-left',
      valueGetter: (params) => {
        const from = params.data?.FromDate
          ? new Date(params.data.FromDate).toLocaleDateString('en-GB')
          : '';
        const to = params.data?.ToDate
          ? new Date(params.data.ToDate).toLocaleDateString('en-GB')
          : '';
        return `${from}  -  ${to}`;
      },
    },
    {
      field: 'TotalHrs',
      headerName: 'TotalHrs',
      width: 80,
      cellClass: 'text-center',
    },
  ];

  dateFormatter(params: ValueFormatterParams): string {
    if (!params.value) return 'N/A';

    const date = new Date(params.value);
    if (isNaN(date.getTime())) return 'Invalid Date';

    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  }
}
