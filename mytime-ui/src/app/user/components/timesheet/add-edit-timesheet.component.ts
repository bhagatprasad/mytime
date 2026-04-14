import { Component, OnInit } from '@angular/core';
import { TimesheetService } from '../../../common/services/timesheet.service';
import { TaskcodeService } from '../../../admin/services/taskcode.service';
import { TaskitemService } from '../../../admin/services/taskitem.service';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { LoaderService } from '../../../common/services/loader.service';
import { AuditFieldsService } from '../../../common/services/auditfields.service';
import { ToastrService } from 'ngx-toastr';
import { forkJoin } from 'rxjs/internal/observable/forkJoin';
import { Timesheet } from '../../../common/models/timesheet';
import { TimesheetTask } from '../../../common/models/timesheet_task';
import { TaskItem } from '../../../admin/models/taskitem';
import { Taskcode } from '../../../admin/models/taskcode';
import { error } from 'console';

@Component({
  selector: 'app-add-edit-timesheet',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './add-edit-timesheet.component.html',
  styleUrl: './add-edit-timesheet.component.css'
})
export class AddEditTimesheetComponent implements OnInit {

  timsheetId: number = 0;
  timehseet: Timesheet | null = null;
  timehseetTasks: TimesheetTask[] = [];
  taskItems: TaskItem[] = [];
  taskCodes: Taskcode[] = [];

  constructor(private timesheetService: TimesheetService,
    private taskItemService: TaskitemService,
    private taskCodeService: TaskcodeService,
    private route: ActivatedRoute,
    private router: Router,
    private loader: LoaderService,
    private audit: AuditFieldsService,
    private toastr: ToastrService) { }

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('timsheetId');
    this.timsheetId = id ? Number(id) : 0;
    this.InitializeTimesheetData();
  }

  InitializeTimesheetData() {
    this.loader.show();

    const requests: any = {
      taskitems: this.taskItemService.GetTaskitemListAsync(),
      taskcodes: this.taskCodeService.getTaskcodeListAsync(),
    };

    if (this.timsheetId && this.timsheetId > 0) {
      requests.timesheet = this.timesheetService.getTimesheetByIdAsync(this.timsheetId);
      requests.timesheetTasks = this.timesheetService.getTimesheetWithTasksAsync(this.timsheetId);
    }

    forkJoin(requests).subscribe({
      next: (response: any) => {
        this.taskItems = response.taskitems || [];
        this.taskCodes = response.taskcodes || [];

        this.timehseet = response.timesheet || null;
        this.timehseetTasks = response.timesheetTasks || [];

        this.loader.hide();
      },
      error: (error) => {
        console.error(error);
        this.loader.hide();
        this.toastr.error('Failed to load timesheet', 'Error');
      }
    });
  }
}


