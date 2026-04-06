import { CommonModule } from '@angular/common';
import { Component, HostListener, OnInit } from '@angular/core';
import { Timesheet } from '../../../common/models/timesheet';
import { TimesheetService } from '../../../common/services/timesheet.service';
import {
  AllCommunityModule,
  ColDef,
  GridApi,
  GridOptions,
  GridReadyEvent,
  ICellRendererParams,
  ModuleRegistry,
} from 'ag-grid-community';
import { AgGridModule } from 'ag-grid-angular';
import { ToastrService } from 'ngx-toastr';
import { LoaderService } from '../../../common/services/loader.service';
import { AddTimesheetComponent } from './add-timesheet.component';
import { ActionsRendererComponent } from '../../../common/components/actions-renderer.component';
import { MobileActionsRendererComponent } from '../../../common/components/mobile-actions-renderer.component';
import { TaskitemService } from '../../../admin/services/taskitem.service';
import { TaskItem } from '../../../admin/models/taskitem';
import { forkJoin } from 'rxjs';
import { Taskcode } from '../../../admin/models/taskcode';
import { TaskcodeService } from '../../../admin/services/taskcode.service';
import { AuditFieldsService } from '../../../common/services/auditfields.service';
import { DeleteConfirmationComponent } from '../../../common/components/delete.compunent';

ModuleRegistry.registerModules([AllCommunityModule]);

@Component({
  selector: 'app-list-timesheet',
  standalone: true,
  imports: [
    CommonModule,
    AgGridModule,
    AddTimesheetComponent,
    DeleteConfirmationComponent,
  ],
  templateUrl: './list-timesheet.component.html',
  styleUrl: './list-timesheet.component.css',
})
export class ListTimesheetComponent implements OnInit {
  timesheets: Timesheet[] = [];
  taskitems: TaskItem[] = [];
  taskcodes: Taskcode[] = [];

  showSidebar = false;
  selectedTimesheet: Timesheet | null = null;
  mode: 'create' | 'edit' = 'create';

  showDeletePopup = false;
  selectedDeleteItem: Timesheet | null = null;

  private gridApi!: GridApi;
  isMobile = false;

  constructor(
    private taskcodeService: TaskcodeService,
    private taskitemService: TaskitemService,
    private timesheetService: TimesheetService,
    private toastr: ToastrService,
    private loader: LoaderService,
    private audit: AuditFieldsService,
  ) {}

  ngOnInit(): void {
    this.checkScreenSize();
    this.setupResponsiveColumns();
    this.loadTimesheetDetails();
  }

  @HostListener('window:resize')
  onResize(): void {
    this.checkScreenSize();
  }

  private checkScreenSize(): void {
    const prev = this.isMobile;
    this.isMobile = window.innerWidth < 768;

    if (prev !== this.isMobile) {
      this.setupResponsiveColumns();
    }
  }

  private setupResponsiveColumns(): void {
    this.columnDefs = this.isMobile
      ? [...this.mobileColumnDefs]
      : [...this.desktopColumnDefs];

    this.gridOptions.domLayout = this.isMobile ? 'autoHeight' : 'normal';

    if (this.gridApi) {
      setTimeout(() => this.gridApi.sizeColumnsToFit(), 100);
    }
  }

  loadTimesheetDetails(): void {
    this.loader.show();

    forkJoin({
      timesheets: this.timesheetService.getTimesheetsListAsync(),
      taskitems: this.taskitemService.GetTaskitemListAsync(),
      taskcodes: this.taskcodeService.getTaskcodeListAsync(),
    }).subscribe({
      next: ({ timesheets, taskitems, taskcodes }) => {
        this.timesheets = timesheets || [];
        this.taskitems = taskitems || [];
        this.taskcodes = taskcodes || [];
        this.loader.hide();

        if (this.gridApi) {
          setTimeout(() => this.gridApi.sizeColumnsToFit(), 100);
        }
      },
      error: (error) => {
        console.error(error);
        this.loader.hide();
        this.toastr.error('Failed to load timesheets', 'Error');
      },
    });
  }

  openAddEditTimesheet(): void {
    this.mode = 'create';
    this.selectedTimesheet = null;
    this.showSidebar = true;
  }

  requestTimesheetProcess(timesheet: any): void {
    console.log('✏️ Edit clicked row:', timesheet);

    this.mode = 'edit';

    this.selectedTimesheet = {
      Id: timesheet.Id,
      FromDate: timesheet.FromDate,
      ToDate: timesheet.ToDate,
      TotalHrs: timesheet.TotalHrs,
      IsActive: timesheet.IsActive,
    };

    console.log('✅ Selected Timesheet for sidebar:', this.selectedTimesheet);

    this.showSidebar = true;
  }

  onCloseSidebar(): void {
    this.showSidebar = false;
    this.selectedTimesheet = null;
  }

  onSaveTimesheet(data: any): void {
    this.loader.show();

    const payload = this.audit.appendAuditFields(data);

    this.timesheetService.insertOrUpdateTimesheet(payload).subscribe({
      next: () => {
        this.toastr.success(
          this.mode === 'create'
            ? 'Timesheet created successfully'
            : 'Timesheet updated successfully',
        );
        this.showSidebar = false;
        this.selectedTimesheet = null;
        this.loadTimesheetDetails();
      },
      error: (error) => {
        console.error(error);
        this.loader.hide();
        this.toastr.error('Something went wrong, please try again');
      },
    });
  }

  deleteTimesheet(timesheet: Timesheet): void {
    this.selectedDeleteItem = timesheet;
    this.showDeletePopup = true;
  }

  closePopup(): void {
    this.showDeletePopup = false;
    this.selectedDeleteItem = null;
  }

  confirmDelete(): void {
    if (!this.selectedDeleteItem?.Id) return;

    this.loader.show();

    this.timesheetService
      .deleteTimesheet(this.selectedDeleteItem.Id)
      .subscribe({
        next: () => {
          this.toastr.success('Timesheet deleted successfully');
          this.closePopup();
          this.loadTimesheetDetails();
        },
        error: (err) => {
          console.error(err);
          this.loader.hide();
          this.toastr.error('Delete failed');
        },
      });
  }

  getTotalRowsCount(): number {
    return this.timesheets.length;
  }

  getActiveTimesheetCount(): number {
    return this.timesheets.filter((x) => x.IsActive).length;
  }

  getInactiveTimesheetCount(): number {
    return this.timesheets.filter((x) => !x.IsActive).length;
  }

  onGridReady(params: GridReadyEvent): void {
    this.gridApi = params.api;
    setTimeout(() => this.gridApi.sizeColumnsToFit(), 200);
  }

  columnDefs: ColDef[] = [];

  defaultColDef: ColDef = {
    flex: 1,
    minWidth: 100,
    filter: true,
    resizable: true,
    sortable: true,
  };

  gridOptions: GridOptions = {
    pagination: true,
    paginationPageSize: 10,
    paginationPageSizeSelector: [10, 20, 50, 100],
    rowSelection: 'single',
    animateRows: true,
    domLayout: 'normal',
  };

  desktopColumnDefs: ColDef[] = [
    { field: 'Id', headerName: 'ID', width: 90, cellClass: 'text-center' },
    {
      headerName: 'Date Range',
      width: 180,
      valueGetter: (params) => {
        const from = params.data?.FromDate
          ? new Date(params.data.FromDate).toLocaleDateString('en-GB')
          : '';
        const to = params.data?.ToDate
          ? new Date(params.data.ToDate).toLocaleDateString('en-GB')
          : '';
        return `${from} - ${to}`;
      },
    },

    { field: 'TotalHrs', headerName: 'Total Hrs', width: 120 },
    {
      field: 'IsActive',
      headerName: 'Status',
      width: 120,
      cellRenderer: this.statusRenderer.bind(this),
    },
    {
      field: 'Actions',
      headerName: 'Actions',
      width: 150,
      sortable: false,
      filter: false,
      cellRenderer: ActionsRendererComponent,
      cellRendererParams: {
        onEditClick: (data: Timesheet) => this.requestTimesheetProcess(data),
        onDeleteClick: (data: Timesheet) => this.deleteTimesheet(data),
      },
      cellClass: 'text-center',
    },
  ];

  mobileColumnDefs: ColDef[] = [
    { field: 'Id', headerName: 'ID', width: 40 },
    {
      headerName: 'Date Range',
      width: 100,
      valueGetter: (params) => {
        const from = params.data?.FromDate
          ? new Date(params.data.FromDate).toLocaleDateString('en-GB')
          : '';
        const to = params.data?.ToDate
          ? new Date(params.data.ToDate).toLocaleDateString('en-GB')
          : '';
        return `${from} - ${to}`;
      },
    },
    { field: 'TotalHrs', headerName: 'Hours', width: 40 },
    // {
    //   field: 'Actions',
    //   headerName: 'Actions',
    //   width: 100,
    //   sortable: false,
    //   filter: false,
    //   cellRenderer: MobileActionsRendererComponent,
    //   cellRendererParams: {
    //     onEditClick: (data: Timesheet) => this.requestTimesheetProcess(data),
    //   },
    // },
  ];

  statusRenderer(params: ICellRendererParams): string {
    return params.value
      ? `<span class="badge bg-success">Active</span>`
      : `<span class="badge bg-danger">Inactive</span>`;
  }
}
