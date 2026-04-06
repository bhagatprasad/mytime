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
  @Input() mode: 'create' | 'edit' = 'create';
  @Input() timesheet: Timesheet | null = null;
  @Input() taskitems: TaskItem[] = [];
  @Input() taskcodes: Taskcode[] = [];

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
    if (changes['mode'] || changes['timesheet']) {
      this.initializeForm();
    }
  }

  initializeForm(): void {
    if (this.mode === 'edit') {
      this.initializeEditForm();
    } else {
      this.initializeCreateForm();
    }
  }

  initializeEditForm(): void {
    this.timesheetForm = this.fb.group({
      FromDate: [
        this.formatDateInput(this.timesheet?.FromDate),
        Validators.required,
      ],
      ToDate: [
        this.formatDateInput(this.timesheet?.ToDate),
        Validators.required,
      ],
      TotalHrs: [this.timesheet?.TotalHrs ?? 0, Validators.required],
      IsActive: [this.timesheet?.IsActive ?? true],
    });
  }

  initializeCreateForm(): void {
    this.timesheetForm = this.fb.group({
      rows: this.fb.array([]),
    });

    if (this.rows.length === 0) {
      this.addRow();
    }
  }

  formatDateInput(date: any): string {
    if (!date) return '';
    const d = new Date(date);
    if (isNaN(d.getTime())) return '';

    const day = String(d.getDate()).padStart(2, '0');
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const year = d.getFullYear();

    return `${day}-${month}-${year}`;
  }

  get rows(): FormArray {
    return this.timesheetForm.get('rows') as FormArray;
  }

  createRow(): FormGroup {
    return this.fb.group({
      taskItem: ['', Validators.required],
      taskCode: ['', Validators.required],
      monday: [0, [Validators.min(0), Validators.max(9)]],
      tuesday: [0, [Validators.min(0), Validators.max(9)]],
      wednesday: [0, [Validators.min(0), Validators.max(9)]],
      thursday: [0, [Validators.min(0), Validators.max(9)]],
      friday: [0, [Validators.min(0), Validators.max(9)]],
      saturday: [{ value: 0, disabled: true }],
      sunday: [{ value: 0, disabled: true }],
    });
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
    this.rows.at(index).get('taskCode')?.setValue('');
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
    const dayOfWeek = date.getDay();
    const diffToMonday = dayOfWeek === 0 ? 6 : dayOfWeek - 1;

    this.weekStart = new Date(date);
    this.weekStart.setDate(date.getDate() - diffToMonday);
    this.weekStart.setHours(0, 0, 0, 0);

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
      Number(row.friday || 0)
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
    if (this.mode === 'edit') {
      if (this.timesheetForm.invalid) {
        this.timesheetForm.markAllAsTouched();
        return;
      }

      const payload = {
        ...this.timesheet,
        ...this.timesheetForm.value,
      };

      this.saveTimesheet.emit(payload);
      return;
    }

    if (this.timesheetForm.invalid) {
      this.showToastMessage('Please fill all required fields', 'error');
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

    const payload = {
      Id: 0,
      Name: `Week ${this.formatDate(this.weekStart)} - ${this.formatDate(this.weekEnd)}`,
      Code: 'WEEKLY',
      FromDate: this.weekStart,
      ToDate: this.weekEnd,
      TotalHrs: this.getWeekTotal(),
      IsActive: true,
      Rows: this.timesheetForm.getRawValue().rows,
    };

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
}
