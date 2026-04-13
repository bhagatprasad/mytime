import { CommonModule } from '@angular/common';
import {
  Component,
  EventEmitter,
  Input,
  OnChanges,
  OnInit,
  Output,
  SimpleChanges,
} from '@angular/core';
import {
  FormArray,
  FormBuilder,
  FormGroup,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import { TaskItem } from '../../../admin/models/taskitem';
import { Taskcode } from '../../../admin/models/taskcode';
import { Timesheet } from '../../../common/models/timesheet';

@Component({
  selector: 'app-add-timesheet',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './add-timesheet.component.html',
  styleUrls: ['./add-timesheet.component.css'],
})
export class AddTimesheetComponent implements OnInit, OnChanges {
  @Input() isVisible = false;
  @Input() timesheet: Timesheet | null = null;
  @Input() taskitems: TaskItem[] = [];
  @Input() taskcodes: Taskcode[] = [];
  @Input() existingTimesheets: Timesheet[] = [];

  @Output() closeSidebar = new EventEmitter<void>();
  @Output() saveTimesheet = new EventEmitter<any>();

  timesheetForm!: FormGroup;

  dailyMin = 8;
  dailyMax = 9;
  weeklyMin = 40;
  weeklyMax = 45;

  weekStart: Date = new Date();
  weekEnd: Date = new Date();

  weekDates = {
    monday: '',
    tuesday: '',
    wednesday: '',
    thursday: '',
    friday: '',
    saturday: '',
    sunday: '',
  };

  currentMonth: Date = new Date();
  currentYear: number = new Date().getFullYear();
  calendarDays: Date[] = [];
  showCalendar = false;

  showDuplicateWeekPopup = false;
  duplicateWeekMessage = '';
  duplicateTimesheet: Timesheet | null = null;

  monthNames = [
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

  toastMessage = '';
  toastType: 'error' | 'warning' | 'success' = 'error';
  showToast = false;

  constructor(private fb: FormBuilder) {
    this.initializeWeekDates();
  }

  ngOnInit(): void {
    this.initializeForm();
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['timesheet'] || changes['isVisible']) {
      if (this.isVisible) {
        console.log('📥 Child received timesheet:', this.timesheet);
        this.initializeForm();
      }
    }
  }

  initializeForm(): void {
    if (this.timesheet?.Id) {
      this.initializeEditForm();
    } else {
      this.initializeCreateForm();
    }
  }

  initializeCreateForm(): void {
    this.initializeWeekDates();

    this.timesheetForm = this.fb.group({
      rows: this.fb.array([]),
    });

    this.rows.clear();
    this.addRow();
  }

  initializeEditForm(): void {
    if (!this.timesheet) return;

    console.log('✏️ FULL TIMESHEET DATA:', this.timesheet);
    console.log('✏️ TASKS ARRAY:', this.timesheet.Tasks);
    console.log('✏️ FIRST TASK HOURS:', this.timesheet.Tasks?.[0]);

    this.weekStart = new Date(this.timesheet.FromDate!);
    this.weekEnd = new Date(this.timesheet.ToDate!);
    this.updateWeekDates();

    this.timesheetForm = this.fb.group({
      rows: this.fb.array([]),
    });

    this.rows.clear();

    const tasks =
      (this.timesheet as any)?.Tasks || (this.timesheet as any)?.tasks || [];

    console.log('📋 Edit mode tasks:', tasks);

    if (tasks && tasks.length > 0) {
      tasks.forEach((task: any) => {
        const row = this.createRow(task);
        this.rows.push(row);
      });
    } else {
      console.warn('⚠️ No task rows found for edit, adding blank row');
      this.addRow();
    }
  }

  get rows(): FormArray {
    return this.timesheetForm.get('rows') as FormArray;
  }

  createRow(task?: any): FormGroup {
    console.log('🏗️ Creating row with task:', task);
    console.log('🏗️ MondayHours:', task?.MondayHours);
    const row = this.fb.group({
      Id: [task?.Id || 0],
      TimesheetId: [task?.TimesheetId || this.timesheet?.Id || 0],
      taskItem: [task?.TaskItemId ?? null, Validators.required],
      taskCode: [task?.TaskCodeId ?? null, Validators.required],
      monday: [task?.MondayHours ?? 0, [Validators.min(0), Validators.max(9)]],
      tuesday: [
        task?.TuesdayHours ?? 0,
        [Validators.min(0), Validators.max(9)],
      ],
      wednesday: [
        task?.WednesdayHours ?? 0,
        [Validators.min(0), Validators.max(9)],
      ],
      thursday: [
        task?.ThursdayHours ?? 0,
        [Validators.min(0), Validators.max(9)],
      ],
      friday: [task?.FridayHours ?? 0, [Validators.min(0), Validators.max(9)]],
      saturday: [{ value: task?.SaturdayHours ?? 0, disabled: true }],
      sunday: [{ value: task?.SundayHours ?? 0, disabled: true }],
      total: [task?.TotalHrs ?? 0],
      IsActive: [task?.IsActive ?? true],
    });

    this.watchRowTotal(row);

    // ensure total recalculates even if backend total missing
    setTimeout(() => {
      this.recalculateSingleRow(row);
    });

    return row;
  }

  watchRowTotal(row: FormGroup): void {
    ['monday', 'tuesday', 'wednesday', 'thursday', 'friday'].forEach((day) => {
      row.get(day)?.valueChanges.subscribe(() => {
        this.recalculateSingleRow(row);
      });
    });
  }

  recalculateSingleRow(row: FormGroup): void {
    const raw = row.getRawValue();
    const total =
      Number(raw.monday || 0) +
      Number(raw.tuesday || 0) +
      Number(raw.wednesday || 0) +
      Number(raw.thursday || 0) +
      Number(raw.friday || 0) +
      Number(raw.saturday || 0) +
      Number(raw.sunday || 0);

    row.get('total')?.setValue(total, { emitEvent: false });
  }

  addRow(): void {
    this.rows.push(this.createRow());
  }

  removeRow(index: number): void {
    if (this.rows.length > 1) {
      this.rows.removeAt(index);
    }
  }

  onTaskItemChange(index: number): void {
    this.rows.at(index).get('taskCode')?.setValue(null);
  }

  getTaskCodes(taskItemId: number): Taskcode[] {
    return this.taskcodes.filter((x) => x.TaskItemId == taskItemId);
  }

  initializeWeekDates(): void {
    const today = new Date();
    const dayOfWeek = today.getDay();
    const diffToMonday = dayOfWeek === 0 ? 6 : dayOfWeek - 1;

    this.weekStart = new Date(today);
    this.weekStart.setDate(today.getDate() - diffToMonday);
    this.weekStart.setHours(0, 0, 0, 0);

    this.updateWeekDates();
  }

  updateWeekDates(): void {
    const weekDays = [
      'monday',
      'tuesday',
      'wednesday',
      'thursday',
      'friday',
      'saturday',
      'sunday',
    ];

    weekDays.forEach((day, index) => {
      const date = new Date(this.weekStart);
      date.setDate(this.weekStart.getDate() + index);
      this.weekDates[day as keyof typeof this.weekDates] =
        this.formatDate(date);
    });

    this.weekEnd = new Date(this.weekStart);
    this.weekEnd.setDate(this.weekStart.getDate() + 6);
  }

  formatDate(date: Date): string {
    const d = date.getDate().toString().padStart(2, '0');
    const m = (date.getMonth() + 1).toString().padStart(2, '0');
    return `${d}/${m}/${date.getFullYear()}`;
  }

  formatDateForDisplay(date: Date): string {
    return `${this.monthNames[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;
  }

  toggleCalendar(): void {
    if (this.timesheet?.Id) return;

    this.showCalendar = !this.showCalendar;
    if (this.showCalendar) {
      this.currentMonth = new Date(this.weekStart);
      this.currentYear = this.currentMonth.getFullYear();
      this.generateCalendarDays();
    }
  }

  generateCalendarDays(): void {
    this.calendarDays = [];
    const firstDayOfMonth = new Date(
      this.currentYear,
      this.currentMonth.getMonth(),
      1,
    );
    const startDate = new Date(firstDayOfMonth);
    startDate.setDate(startDate.getDate() - startDate.getDay());

    for (let i = 0; i < 42; i++) {
      const date = new Date(startDate);
      date.setDate(startDate.getDate() + i);
      this.calendarDays.push(date);
    }
  }

  previousMonth(): void {
    this.currentMonth = new Date(
      this.currentYear,
      this.currentMonth.getMonth() - 1,
      1,
    );
    this.currentYear = this.currentMonth.getFullYear();
    this.generateCalendarDays();
  }

  nextMonth(): void {
    this.currentMonth = new Date(
      this.currentYear,
      this.currentMonth.getMonth() + 1,
      1,
    );
    this.currentYear = this.currentMonth.getFullYear();
    this.generateCalendarDays();
  }

  selectWeekFromCalendar(date: Date): void {
    if (this.timesheet?.Id) return;

    const dayOfWeek = date.getDay();
    const diffToMonday = dayOfWeek === 0 ? 6 : dayOfWeek - 1;

    const selectedWeekStart = new Date(date);
    selectedWeekStart.setDate(date.getDate() - diffToMonday);
    selectedWeekStart.setHours(0, 0, 0, 0);

    const selectedWeekEnd = new Date(selectedWeekStart);
    selectedWeekEnd.setDate(selectedWeekStart.getDate() + 6);

    const existing = this.getExistingWeekTimesheet(
      selectedWeekStart,
      selectedWeekEnd,
    );

    if (existing) {
      this.duplicateTimesheet = existing;
      this.duplicateWeekMessage = `Timesheet already exists for ${this.formatDateForDisplay(selectedWeekStart)} - ${this.formatDateForDisplay(selectedWeekEnd)}`;
      this.showDuplicateWeekPopup = true;
      return;
    }

    this.weekStart = selectedWeekStart;
    this.weekEnd = selectedWeekEnd;

    this.updateWeekDates();
    this.showCalendar = false;
  }

  isCurrentMonth(date: Date): boolean {
    return date.getMonth() === this.currentMonth.getMonth();
  }

  isSelectedWeek(date: Date): boolean {
    return date >= this.weekStart && date <= this.weekEnd;
  }

  getRowTotal(row: any): number {
    return (
      Number(row.monday || 0) +
      Number(row.tuesday || 0) +
      Number(row.wednesday || 0) +
      Number(row.thursday || 0) +
      Number(row.friday || 0) +
      Number(row.saturday || 0) +
      Number(row.sunday || 0)
    );
  }

  getDayTotal(day: string): number {
    return this.rows.controls.reduce((total, row) => {
      const rowValue = row.getRawValue();
      return total + Number(rowValue[day] || 0);
    }, 0);
  }

  getWeekTotal(): number {
    return this.rows.controls.reduce((total, row) => {
      return total + this.getRowTotal(row.getRawValue());
    }, 0);
  }

  validateHourEntry(rowIndex: number, day: string, event: any): void {
    const value = parseFloat(event.target.value) || 0;
    const row = this.rows.at(rowIndex);

    const taskItemId = row.get('taskItem')?.value;
    if (!taskItemId) {
      this.showToastMessage('Please select Task Item first', 'error');
      row.get(day)?.setValue(0);
      return;
    }

    if (value < 0 || value > 9) {
      this.showToastMessage(
        `${this.capitalize(day)} must be between 0 and 9 hours`,
        'error',
      );
      row.get(day)?.setValue(0);
      return;
    }

    const otherRowsTotal = this.rows.controls.reduce((total, r, index) => {
      if (index === rowIndex) return total;
      return total + Number(r.get(day)?.value || 0);
    }, 0);

    const newDayTotal = otherRowsTotal + value;

    if (newDayTotal > this.dailyMax) {
      const allowed = this.dailyMax - otherRowsTotal;
      this.showToastMessage(
        `${this.capitalize(day)} already has ${otherRowsTotal} hrs. You can enter only ${allowed > 0 ? allowed : 0} more hr(s).`,
        'error',
      );
      row.get(day)?.setValue(0);
      return;
    }

    row.get(day)?.setValue(value);
  }

  getDayWarning(day: string): string {
    const total = this.getDayTotal(day);

    if (total === 0) return '';
    if (total === 8 || total === 9) return '';
    if (total > 0 && total < 8) return `Needs ${8 - total}h more`;
    if (total > 9) return 'Exceeded';

    return '';
  }

  getDayHeaderClass(day: string): string {
    const total = this.getDayTotal(day);

    if (total > this.dailyMax) return 'cell-exceeded';
    if (total >= this.dailyMin && total <= this.dailyMax)
      return 'cell-completed';
    if (total > 0 && total < this.dailyMin) return 'cell-incomplete';

    return '';
  }

  hasSubmitErrors(): boolean {
    const days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday'];

    for (const day of days) {
      const total = this.getDayTotal(day);
      if (total > 0 && total < this.dailyMin) return true;
      if (total > this.dailyMax) return true;
    }

    return false;
  }

  isWeekValid(): boolean {
    const total = this.getWeekTotal();
    return total >= this.weeklyMin && total <= this.weeklyMax;
  }

  submitTimesheet(): void {
    if (this.timesheetForm.invalid) {
      this.showToastMessage('Please fill all required fields', 'error');
      this.timesheetForm.markAllAsTouched();
      return;
    }

    if (this.hasSubmitErrors()) {
      this.showToastMessage(
        'Each entered day total must be 8 or 9 hrs only',
        'error',
      );
      return;
    }

    if (!this.isWeekValid()) {
      this.showToastMessage(
        `Weekly total (${this.getWeekTotal()} hrs) should be between ${this.weeklyMin} and ${this.weeklyMax} hrs`,
        'error',
      );
      return;
    }

    // Get rows
    const rawRows = this.timesheetForm.getRawValue().rows;
    console.log('🟦 Raw Rows:', rawRows);

    //  Filter valid rows only
    const validRows = rawRows.filter(
      (row: any) => row.taskItem && row.taskCode,
    );

    console.log('🟩 Valid Rows:', validRows);

    //  If no valid rows → stop
    if (!validRows.length) {
      this.showToastMessage('Please select Task Item and Task Code', 'error');
      return;
    }

    //  Build payload
    const payload = {
      Id: this.timesheet?.Id || 0,
      FromDate: this.weekStart,
      ToDate: this.weekEnd,
      Description: 'Timesheet Entry',
      Status: 'Submitted',
      TotalHrs: this.getWeekTotal(),
      IsActive: true,

      Tasks: validRows.map((row: any) => ({
        Id: row.Id || 0,
        TimesheetId: row.TimesheetId || this.timesheet?.Id || 0,
        TaskItemId: row.taskItem,
        TaskCodeId: row.taskCode,
        MondayHours: Number(row.monday || 0),
        TuesdayHours: Number(row.tuesday || 0),
        WednesdayHours: Number(row.wednesday || 0),
        ThursdayHours: Number(row.thursday || 0),
        FridayHours: Number(row.friday || 0),
        SaturdayHours: Number(row.saturday || 0),
        SundayHours: Number(row.sunday || 0),
        TotalHrs: Number(row.total || 0),
        IsActive: row.IsActive ?? true,
      })),
    };

    console.log('📤 FINAL Payload:', payload);

    // Emit
    this.saveTimesheet.emit(payload);
  }

  close(): void {
    this.closeSidebar.emit();
  }

  showToastMessage(
    message: string,
    type: 'error' | 'warning' | 'success',
  ): void {
    this.toastMessage = message;
    this.toastType = type;
    this.showToast = true;
    setTimeout(() => this.hideToast(), 2500);
  }

  hideToast(): void {
    this.showToast = false;
    this.toastMessage = '';
  }

  capitalize(day: string): string {
    return day.charAt(0).toUpperCase() + day.slice(1);
  }

  normalizeDate(date: Date): Date {
    const d = new Date(date);
    d.setHours(0, 0, 0, 0);
    return d;
  }

  isWeekAlreadyExists(startDate: Date, endDate: Date): boolean {
    const selectedFrom = this.normalizeDate(startDate);
    const selectedTo = this.normalizeDate(endDate);

    return this.existingTimesheets.some((t) => {
      if (!t.FromDate || !t.ToDate) return false;

      const existingFrom = this.normalizeDate(new Date(t.FromDate));
      const existingTo = this.normalizeDate(new Date(t.ToDate));

      return (
        existingFrom.getTime() === selectedFrom.getTime() &&
        existingTo.getTime() === selectedTo.getTime()
      );
    });
  }

  getExistingWeekTimesheet(startDate: Date, endDate: Date): Timesheet | null {
    const selectedFrom = this.normalizeDate(startDate);
    const selectedTo = this.normalizeDate(endDate);

    return (
      this.existingTimesheets.find((t) => {
        if (!t.FromDate || !t.ToDate) return false;

        const existingFrom = this.normalizeDate(new Date(t.FromDate));
        const existingTo = this.normalizeDate(new Date(t.ToDate));

        return (
          existingFrom.getTime() === selectedFrom.getTime() &&
          existingTo.getTime() === selectedTo.getTime()
        );
      }) || null
    );
  }

  closeDuplicatePopup(): void {
    this.showDuplicateWeekPopup = false;
    this.duplicateWeekMessage = '';
    this.duplicateTimesheet = null;
  }

  chooseAnotherWeek(): void {
    this.closeDuplicatePopup();
  }
  trackByIndex(index: number, item: any): number {
    return index;
  }
}
