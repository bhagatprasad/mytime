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
export class ListTimesheetComponent implements OnInit, OnDestroy {
  timesheets: Timesheet[] = [];
  taskitems: TaskItem[] = [];
  taskcodes: Taskcode[] = [];

  showSidebar = false;
  selectedTimesheet: Timesheet | null = null;

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
  ngOnDestroy(): void {
    window.removeEventListener('resize', this.onResize.bind(this));
  }

  ngOnInit(): void {
    this.checkScreenSize();
    this.setupResponsiveColumns();
    this.loadTimesheetDetails();
    window.addEventListener('resize', this.onResize.bind(this));
  }

  @HostListener('window:resize', ['$event'])
  onResize(event: any): void {
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

  loadTimesheetDetails(): void {
    this.loader.show();

    forkJoin({
      timesheets: this.timesheetService.getTimesheetsListAsync(),
      taskitems: this.taskitemService.GetTaskitemListAsync(),
      taskcodes: this.taskcodeService.getTaskcodeListAsync(),
    }).subscribe({
      next: ({ timesheets, taskitems, taskcodes }) => {
        this.timesheets = timesheets;
        this.taskitems = taskitems;
        this.taskcodes = taskcodes;
        this.loader.hide();

        if (this.gridApi) {
          setTimeout(() => this.gridApi.sizeColumnsToFit(), 100);
        }
      },
      error: (error) => {
        console.error('Error Loading Data: ', error);
        this.loader.hide();
        this.toastr.error('Failed to load timesheets', 'Error');
      },
    });
  }

  openAddEditTimesheet(): void {
    this.showSidebar = true;
    this.selectedTimesheet = null;
  }

  requestTimesheetProcess(timesheet: any): void {
    console.log('✏️ Edit clicked row:', timesheet);
    this.loader.show();

    this.timesheetService.getTimesheetWithTasksAsync(timesheet.Id).subscribe({
      next: (res: any) => {
        this.selectedTimesheet = {
          Id: res.Id,
          FromDate: res.FromDate,
          ToDate: res.ToDate,
          TotalHrs: res.TotalHrs,
          IsActive: res.IsActive,
          Tasks: res.Tasks || res.tasks || [],
        };

        this.loader.hide();
        this.showSidebar = true;
      },
      error: (err) => {
        console.error('❌ Error fetching timesheet with tasks:', err);
        this.loader.hide();
        this.toastr.error('Failed to load timesheet details');
      },
    });
  }

  // requestTimesheetProcess(timesheet: Timesheet): void {
  //   this.showSidebar = true;
  //   this.selectedTimesheet = timesheet;
  // }

  onCloseSidebar(): void {
    this.showSidebar = false;
    this.selectedTimesheet = null;
  }

  onSaveTimesheet(payload: any): void {
    this.loader.show();
    console.log('📤 Final payload from child:', payload);

    const parentPayload = {
      Id: payload.Id || 0,
      FromDate: payload.FromDate,
      ToDate: payload.ToDate,
      Description: payload.Description || 'Timesheet Entry',
      EmployeeId: undefined,
      UserId: undefined,
      Status: payload.Status || 'Submitted',
      IsActive: payload.IsActive ?? true,
      TotalHrs: payload.TotalHrs,
      CreatedBy: 21,
      CreatedOn: new Date(),
      ModifiedBy: 21,
      ModifiedOn: new Date(),
    };

    // Save parent
    this.timesheetService.insertOrUpdateTimesheet(parentPayload).subscribe({
      next: (res: any) => {
        console.log('✅ Parent saved:', res);

        const savedTimesheetId =
          res?.timesheet?.Id || // ⭐ MAIN FIX
          res?.Id ||
          res?.id ||
          payload.Id ||
          this.selectedTimesheet?.Id;

        console.log('Saved Timesheet ID:', savedTimesheetId);

        if (!savedTimesheetId) {
          this.loader.hide();
          this.toastr.error('Timesheet ID not found');
          return;
        }

        const tasks = payload.Tasks || [];
        console.log('🟨 Tasks:', tasks);

        // If no tasks
        if (!tasks.length) {
          this.loader.hide();
          this.toastr.success('Timesheet saved successfully');
          this.onCloseSidebar();
          this.loadTimesheetDetails();
          return;
        }

        // Save tasks
        let completed = 0;
        let hasError = false;

        tasks.forEach((task: any) => {
          const taskPayload = {
            Id: task.Id || 0,
            TimesheetId: savedTimesheetId,
            TaskItemId: Number(task.TaskItemId),
            TaskCodeId: Number(task.TaskCodeId),
            MondayHours: Number(task.MondayHours || 0),
            TuesdayHours: Number(task.TuesdayHours || 0),
            WednesdayHours: Number(task.WednesdayHours || 0),
            ThursdayHours: Number(task.ThursdayHours || 0),
            FridayHours: Number(task.FridayHours || 0),
            SaturdayHours: Number(task.SaturdayHours || 0),
            SundayHours: Number(task.SundayHours || 0),
            TotalHrs: Number(task.TotalHrs || 0),
            IsActive: task.IsActive ?? true,
            CreatedBy: 21,
            CreatedOn: new Date(),
            ModifiedBy: 21,
            ModifiedOn: new Date(),
          };

          console.log('🟧 Saving task:', taskPayload);

          this.timesheetService
            .addTimesheetTask(savedTimesheetId, taskPayload)
            .subscribe({
              next: () => {
                completed++;

                if (completed === tasks.length && !hasError) {
                  this.loader.hide();
                  this.toastr.success('Timesheet saved successfully');
                  this.onCloseSidebar();
                  this.loadTimesheetDetails();
                }
              },
              error: (err) => {
                console.error('❌ Task save error:', err);
                hasError = true;
                this.loader.hide();
                this.toastr.error('Task save failed');
              },
            });
        });
      },

      error: (err: any) => {
        console.error('❌ Parent save error:', err);
        this.loader.hide();
        this.toastr.error('Failed to save timesheet');
      },
    });
  }

  refreshData() {
    (this, this.loadTimesheetDetails());
  }

  deleteTimesheet(timesheet: Timesheet): void {
    this.showDeletePopup = true;
    this.selectedDeleteItem = timesheet;
  }

  closePopup(): void {
    this.showDeletePopup = false;
    this.selectedDeleteItem = null;
  }

  confirmDelete(): void {
    if (!this.selectedDeleteItem?.Id) {
      console.error('No valid item selected for delete');
      return;
    }

    this.loader.show();

    this.timesheetService
      .deleteTimesheet(this.selectedDeleteItem.Id)
      .subscribe({
        next: () => {
          this.loader.hide();
          this.toastr.success('Deleted successfully');
          this.closePopup();
          this.selectedDeleteItem = null;
          this.loadTimesheetDetails();
        },
        error: (err) => {
          console.error('Delete failed:', err);
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

    {
      field: 'TotalHrs',
      headerName: 'Total(Hrs)',
      width: 90,
      cellClass: 'text-center',
    },
    { field: 'Description', headerName: 'Description', width: 160 },
    {
      field: 'IsActive',
      headerName: 'Status',
      width: 120,
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
        onEditClick: (data: Timesheet) => this.requestTimesheetProcess(data),
        onDeleteClick: (data: Timesheet) => this.deleteTimesheet(data),
      },
      cellClass: 'text-center',
    },
  ];

  mobileColumnDefs: ColDef[] = [
    { field: 'Id', headerName: 'ID', width: 20 },
    {
      headerName: 'Date Range',
      width: 70,
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
    { field: 'TotalHrs', headerName: 'Hours', width: 20 },
    {
      field: 'Actions',
      headerName: 'Actions',
      width: 120,
      sortable: false,
      filter: false,
      cellRenderer: MobileActionsRendererComponent,
      cellRendererParams: {
        onEditClick: (data: Timesheet) => this.requestTimesheetProcess(data),
        onDeleteClick: (data: Timesheet) => this.deleteTimesheet(data),
      },
      cellClass: 'text-center',
    },
  ];

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
  statusCellClass(params: any): string {
    const isActive = params.value;
    return isActive ? 'status-active' : 'status-inactive';
  }
}
