import { Component, OnInit } from '@angular/core';
import { TimesheetService } from '../../../common/services/timesheet.service';
import { TaskcodeService } from '../../../admin/services/taskcode.service';
import { TaskitemService } from '../../../admin/services/taskitem.service';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { LoaderService } from '../../../common/services/loader.service';
import { AuditFieldsService } from '../../../common/services/auditfields.service';
import { ToastrService } from 'ngx-toastr';
import { forkJoin } from 'rxjs';
import { Timesheet } from '../../../common/models/timesheet';
import { TimesheetTask } from '../../../common/models/timesheet_task';
import { TaskItem } from '../../../admin/models/taskitem';
import { Taskcode } from '../../../admin/models/taskcode';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-add-edit-timesheet',
  standalone: true,
  imports: [CommonModule, RouterModule, FormsModule],
  templateUrl: './add-edit-timesheet.component.html',
  styleUrl: './add-edit-timesheet.component.css',
})
export class AddEditTimesheetComponent implements OnInit {
  timsheetId: number = 0;
  timehseet: Timesheet | null = null;
  timehseetTasks: TimesheetTask[] = [];
  taskItems: TaskItem[] = [];
  taskCodes: Taskcode[] = [];

  // ✅ Fast lookup maps
  taskItemMap = new Map<number, string>();
  taskCodeMap = new Map<number, string>();

  constructor(
    private timesheetService: TimesheetService,
    private taskItemService: TaskitemService,
    private taskCodeService: TaskcodeService,
    private route: ActivatedRoute,
    private router: Router,
    private loader: LoaderService,
    private audit: AuditFieldsService,
    private toastr: ToastrService,
  ) {}

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('timsheetId');
    this.timsheetId = id ? Number(id) : 0;

    console.log('Timesheet ID:', this.timsheetId);

    this.InitializeTimesheetData();
  }

  InitializeTimesheetData() {
    this.loader.show();

    const requests: any = {
      taskitems: this.taskItemService.GetTaskitemListAsync(),
      taskcodes: this.taskCodeService.getTaskcodeListAsync(),
    };

    if (this.timsheetId && this.timsheetId > 0) {
      requests.timesheet = this.timesheetService.getTimesheetByIdAsync(
        this.timsheetId,
      );

      requests.timesheetTasks =
        this.timesheetService.getTimesheetWithTasksAsync(this.timsheetId);
    }

    forkJoin(requests).subscribe({
      next: (response: any) => {
        try {
          console.log('FULL RESPONSE:', response);

          // ✅ Assign master data
          this.taskItems = response.taskitems || [];
          this.taskCodes = response.taskcodes || [];

          // ✅ Build maps (important)
          this.taskItems.forEach((item) => {
            this.taskItemMap.set(item.TaskItemId, item.Name);
          });

          this.taskCodes.forEach((code) => {
            this.taskCodeMap.set(code.TaskCodeId, code.Name);
          });

          // ✅ Assign timesheet
          this.timehseet = response.timesheet || null;

          if (this.timehseet) {
            this.patchDates();
          }

          // ✅ CRITICAL FIX (NO MORE NG0900 ERROR)
          if (Array.isArray(response.timesheetTasks)) {
            this.timehseetTasks = response.timesheetTasks;
          } else if (response.timesheetTasks) {
            this.timehseetTasks = [response.timesheetTasks];
          } else {
            this.timehseetTasks = [];
          }

          console.log('FINAL TASKS:', this.timehseetTasks);
        } catch (err) {
          console.error('FRONTEND ERROR:', err);
          this.toastr.error('UI rendering error', 'Error');
        } finally {
          this.loader.hide(); // ✅ ALWAYS hide loader
        }
      },

      error: (error) => {
        console.error('API ERROR:', error);
        this.loader.hide();
        this.toastr.error('Failed to load timesheet', 'Error');
      },
    });
  }

  // ✅ Fix date format for input[type=date]
  patchDates() {
    if (!this.timehseet) return;

    this.timehseet.FromDate = this.formatDate(this.timehseet.FromDate);
    this.timehseet.ToDate = this.formatDate(this.timehseet.ToDate);
  }

  formatDate(date: any): string {
    return new Date(date).toISOString().split('T')[0];
  }

  // ✅ Optional (if you still use in HTML)
  getTaskItemName(id: number): string {
    return this.taskItemMap.get(id) || 'N/A';
  }

  getTaskCodeName(id: number): string {
    return this.taskCodeMap.get(id) || 'N/A';
  }
}
