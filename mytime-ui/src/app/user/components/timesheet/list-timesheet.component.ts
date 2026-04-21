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
import { Router } from '@angular/router';

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
    private router: Router,
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
    console.log('🟢 Navigating to edit timesheet ID:', timesheet.Id);
    this.router.navigate(['/user/timesheet', timesheet.Id]);
  }

  onCloseSidebar(): void {
    this.showSidebar = false;
    this.selectedTimesheet = null;
  }

  onSaveTimesheet(payload: any): void {
    console.log('📤 Final payload from child:', payload);
    this.loader.show();

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

    console.log('🟦 Saving parent Timesheet:', parentPayload);

    this.timesheetService.insertOrUpdateTimesheet(parentPayload).subscribe({
      next: (res: any) => {
        console.log('✅ Parent Timesheet response:', res);

        // Get the saved Timesheet ID
        const savedTimesheetId =
          res?.Id || res?.timesheet?.Id || res?.id || payload.Id;
        console.log('🔥 Saved Timesheet ID:', savedTimesheetId);

        if (!savedTimesheetId) {
          this.loader.hide();
          this.toastr.error('Timesheet saved but ID not found');
          return;
        }

        const tasks = payload.Tasks || [];
        console.log('🟨 Tasks to save:', tasks);
        console.log('🟨 Number of tasks:', tasks.length);

        if (!tasks.length) {
          this.loader.hide();
          this.toastr.success('Timesheet saved successfully (no tasks)');
          this.onCloseSidebar();
          this.loadTimesheetDetails();
          return;
        }

        let completed = 0;
        let hasError = false;

        // Save each task to TimesheetTask table
        tasks.forEach((task: any, index: number) => {
          console.log(`🟧 Saving task ${index + 1}:`, task);

          const taskPayload = {
            TimesheetId: savedTimesheetId,
            TaskItemId: task.TaskItemId,
            TaskCodeId: task.TaskCodeId,
            MondayHours: Number(task.MondayHours || 0),
            TuesdayHours: Number(task.TuesdayHours || 0),
            WednesdayHours: Number(task.WednesdayHours || 0),
            ThursdayHours: Number(task.ThursdayHours || 0),
            FridayHours: Number(task.FridayHours || 0),
            SaturdayHours: Number(task.SaturdayHours || 0),
            SundayHours: Number(task.SundayHours || 0),
            TotalHrs: Number(task.TotalHrs || 0),
            IsActive: true,
            CreatedBy: 21,
            CreatedOn: new Date(),
            ModifiedBy: 21,
            ModifiedOn: new Date(),
          };

          console.log('📤 Task Payload being sent:', taskPayload);

          this.timesheetService.addTimesheetTask(savedTimesheetId, taskPayload);
          this.timesheetService
            .insertOrUpdateTimesheetTask(taskPayload)
            .subscribe({
              next: (taskRes: any) => {
                console.log(
                  `✅ Task ${index + 1} saved successfully:`,
                  taskRes,
                );
                completed++;

                if (completed === tasks.length && !hasError) {
                  console.log('🎉 All tasks saved successfully!');
                  this.loader.hide();
                  this.toastr.success(
                    this.mode === 'edit'
                      ? 'Timesheet updated successfully'
                      : 'Timesheet created successfully',
                  );
                  this.onCloseSidebar();
                  this.loadTimesheetDetails();
                }
              },
              error: (taskErr: any) => {
                console.error(`❌ Error saving task ${index + 1}:`, taskErr);
                hasError = true;
                this.loader.hide();
                this.toastr.error(`Task ${index + 1} failed to save`);
              },
            });
        });
      },
      error: (err: any) => {
        console.error('❌ Error saving parent timesheet:', err);
        this.loader.hide();
        this.toastr.error('Failed to save timesheet');
      },
    });
  }
  saveTaskRows(timesheetId: number, tasks: any[]): void {
    const requests = tasks.map((task) => {
      const taskPayload = {
        TimesheetId: timesheetId,
        TaskItemId: Number(task.taskItem),
        TaskCodeId: Number(task.taskCode),
        MondayHours: Number(task.monday || 0),
        TuesdayHours: Number(task.tuesday || 0),
        WednesdayHours: Number(task.wednesday || 0),
        ThursdayHours: Number(task.thursday || 0),
        FridayHours: Number(task.friday || 0),
        SaturdayHours: Number(task.saturday || 0),
        SundayHours: Number(task.sunday || 0),
        TotalHrs:
          Number(task.monday || 0) +
          Number(task.tuesday || 0) +
          Number(task.wednesday || 0) +
          Number(task.thursday || 0) +
          Number(task.friday || 0) +
          Number(task.saturday || 0) +
          Number(task.sunday || 0),
        IsActive: true,
      };

      return this.timesheetService.addTimesheetTask(timesheetId, taskPayload);
    });

    forkJoin(requests).subscribe({
      next: () => {
        this.loader.hide();
        this.toastr.success('Timesheet and tasks saved successfully');
        this.showSidebar = false;
        this.selectedTimesheet = null;
        this.loadTimesheetDetails();
      },
      error: (error) => {
        console.error(error);
        this.loader.hide();
        this.toastr.error('Parent saved, but task rows failed');
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
    return params.value
      ? `<span class="badge bg-success">Active</span>`
      : `<span class="badge bg-danger">Inactive</span>`;
  }
}
