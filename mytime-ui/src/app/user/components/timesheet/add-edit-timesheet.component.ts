import { Component, OnInit } from '@angular/core';
import { TimesheetService } from '../../../common/services/timesheet.service';
import { TaskcodeService } from '../../../admin/services/taskcode.service';
import { TaskitemService } from '../../../admin/services/taskitem.service';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { LoaderService } from '../../../common/services/loader.service';
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
  styleUrls: ['./add-edit-timesheet.component.css'],
})
export class AddEditTimesheetComponent implements OnInit {
  // ========== PROPERTIES ==========
  timsheetId: number = 0;
  timehseet: Timesheet | null = null;
  timehseetTasks: TimesheetTask[] = [];
  taskItems: TaskItem[] = [];
  taskCodes: Taskcode[] = [];

  weeklyMin = 40;
  weeklyMax = 45;
  dailyMin = 8;
  dailyMax = 9;

  weekDays = [
    { name: 'Mon', key: 'monday' },
    { name: 'Tue', key: 'tuesday' },
    { name: 'Wed', key: 'wednesday' },
    { name: 'Thu', key: 'thursday' },
    { name: 'Fri', key: 'friday' },
    { name: 'Sat', key: 'saturday' },
    { name: 'Sun', key: 'sunday' },
  ];

  // ========== CONSTRUCTOR ==========
  constructor(
    private timesheetService: TimesheetService,
    private taskItemService: TaskitemService,
    private taskCodeService: TaskcodeService,
    private route: ActivatedRoute,
    private router: Router,
    private loader: LoaderService,
    private toastr: ToastrService,
  ) {}

  // ========== LIFE CYCLE HOOKS ==========
  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('timesheetId');
    this.timsheetId = id ? Number(id) : 0;

    if (!this.timsheetId) {
      this.toastr.error('Invalid timesheet ID');
      this.goBack();
      return;
    }

    this.loadData();
  }

  // ========== DATA LOADING ==========
  loadData(): void {
    this.loader.show();

    forkJoin({
      timesheet: this.timesheetService.getTimesheetByIdAsync(this.timsheetId),
      tasks: this.timesheetService.getTimesheetWithTasksAsync(this.timsheetId),
      taskItems: this.taskItemService.GetTaskitemListAsync(),
      taskCodes: this.taskCodeService.getTaskcodeListAsync(),
    }).subscribe({
      next: ({ timesheet, tasks, taskItems, taskCodes }) => {
        console.log('📋 Loaded timesheet:', timesheet);
        console.log('📋 Loaded tasks:', tasks);

        this.timehseet = timesheet;
        this.taskItems = taskItems || [];
        this.taskCodes = taskCodes || [];

        // Handle tasks - ensure it's an array
        if (Array.isArray(tasks)) {
          this.timehseetTasks = tasks;
        } else if (tasks && (tasks as any).Tasks) {
          this.timehseetTasks = (tasks as any).Tasks;
        } else {
          this.timehseetTasks = [];
        }

        // If no tasks, add an empty row
        if (this.timehseetTasks.length === 0) {
          this.addNewTask();
        }

        this.loader.hide();
      },
      error: (error) => {
        console.error('Error loading data:', error);
        this.loader.hide();
        this.toastr.error('Failed to load timesheet data');
        this.goBack();
      },
    });
  }

  // ========== TASK CODE FILTERING ==========
  getFilteredTaskCodes(taskItemId: number | undefined): Taskcode[] {
    if (!taskItemId) return [];
    return this.taskCodes.filter((code) => code.TaskItemId === taskItemId);
  }

  onTaskItemChange(index: number): void {
    if (this.timehseetTasks[index]) {
      this.timehseetTasks[index].TaskCodeId = undefined;
    }
  }

  // ========== CALCULATIONS ==========
  calculateTaskTotal(task: TimesheetTask): number {
    const total =
      (task.MondayHours || 0) +
      (task.TuesdayHours || 0) +
      (task.WednesdayHours || 0) +
      (task.ThursdayHours || 0) +
      (task.FridayHours || 0) +
      (task.SaturdayHours || 0) +
      (task.SundayHours || 0);

    task.TotalHrs = total;
    return total;
  }

  recalculateTotal(index: number): void {
    if (this.timehseetTasks[index]) {
      this.calculateTaskTotal(this.timehseetTasks[index]);
    }
  }

  getWeekTotal(): number {
    if (!this.timehseetTasks) return 0;
    return this.timehseetTasks.reduce((sum, task) => {
      return sum + (task.TotalHrs || 0);
    }, 0);
  }

  getDayTotal(day: string): number {
    return this.timehseetTasks.reduce((total, task) => {
      const hours = (task[day as keyof TimesheetTask] as number) || 0;
      return total + hours;
    }, 0);
  }

  // ========== VALIDATIONS ==========
  isWeekValid(): boolean {
    const total = this.getWeekTotal();
    return total >= this.weeklyMin && total <= this.weeklyMax;
  }

  isFormValid(): boolean {
    if (!this.timehseet?.Description?.trim()) return false;
    if (!this.isWeekValid()) return false;

    for (const task of this.timehseetTasks) {
      if (!task.TaskItemId || !task.TaskCodeId) return false;
    }

    return true;
  }

  getDayHeaderClass(day: string): string {
    const total = this.getDayTotal(day);
    if (total > this.dailyMax) return 'cell-exceeded';
    if (total >= this.dailyMin && total <= this.dailyMax)
      return 'cell-completed';
    if (total > 0 && total < this.dailyMin) return 'cell-incomplete';
    return '';
  }

  // ========== TASK ROW MANAGEMENT ==========
  addNewTask(): void {
    const newTask: TimesheetTask = {
      Id: 0,
      TimesheetId: this.timsheetId,
      TaskItemId: undefined,
      TaskCodeId: undefined,
      MondayHours: 0,
      TuesdayHours: 0,
      WednesdayHours: 0,
      ThursdayHours: 0,
      FridayHours: 0,
      SaturdayHours: 0,
      SundayHours: 0,
      TotalHrs: 0,
      IsActive: true,
    };
    this.timehseetTasks.push(newTask);
  }

  removeTask(index: number): void {
    if (this.timehseetTasks.length > 1) {
      this.timehseetTasks.splice(index, 1);
    }
  }

  // ========== DATE FORMATTING ==========
  formatDateForDisplay(date: any): string {
    if (!date) return '';
    const d = new Date(date);
    const months = [
      'January',
      'February',
      'March',
      'April',
      'May',
      'June',
      'July',
      'August',
      'September',
      'October',
      'November',
      'December',
    ];
    return `${months[d.getMonth()]} ${d.getDate()}, ${d.getFullYear()}`;
  }

  getFormattedDateForDay(offset: number): string {
    if (!this.timehseet?.FromDate) return '';
    const date = new Date(this.timehseet.FromDate);
    date.setDate(date.getDate() + offset);
    return `${date.getDate()}/${date.getMonth() + 1}/${date.getFullYear()}`;
  }

  // ========== UPDATE TIMESHEET ==========
  updateTimesheet(): void {
    if (!this.isFormValid()) {
      this.toastr.warning(
        'Please fill all required fields and ensure weekly total is between 40-45 hours',
      );
      return;
    }

    this.loader.show();

    const parentPayload = {
      Id: this.timehseet?.Id || 0,
      FromDate: this.timehseet?.FromDate,
      ToDate: this.timehseet?.ToDate,
      Description: this.timehseet?.Description,
      Status: this.timehseet?.Status || 'Submitted',
      TotalHrs: this.getWeekTotal(),
      IsActive: true,
    };

    this.timesheetService.insertOrUpdateTimesheet(parentPayload).subscribe({
      next: (res: any) => {
        const savedId = res?.Id || res?.timesheet?.Id || this.timsheetId;

        if (!savedId) {
          this.loader.hide();
          this.toastr.error('Failed to save timesheet');
          return;
        }

        const taskRequests = this.timehseetTasks.map((task) => {
          const taskPayload = {
            Id: task.Id || 0,
            TimesheetId: savedId,
            TaskItemId: task.TaskItemId,
            TaskCodeId: task.TaskCodeId,
            MondayHours: task.MondayHours || 0,
            TuesdayHours: task.TuesdayHours || 0,
            WednesdayHours: task.WednesdayHours || 0,
            ThursdayHours: task.ThursdayHours || 0,
            FridayHours: task.FridayHours || 0,
            SaturdayHours: task.SaturdayHours || 0,
            SundayHours: task.SundayHours || 0,
            TotalHrs: this.calculateTaskTotal(task),
            IsActive: true,
          };
          return this.timesheetService.addTimesheetTask(savedId, taskPayload);
        });

        forkJoin(taskRequests).subscribe({
          next: () => {
            this.loader.hide();
            this.toastr.success('Timesheet updated successfully');
            this.goBack();
          },
          error: (err) => {
            console.error('Task save error:', err);
            this.loader.hide();
            this.toastr.error('Timesheet saved but tasks failed');
          },
        });
      },
      error: (err) => {
        console.error('Update error:', err);
        this.loader.hide();
        this.toastr.error('Failed to update timesheet');
      },
    });
  }

  // ========== NAVIGATION ==========
  goBack(): void {
    this.router.navigate(['/user/timesheet']);
  }
}
