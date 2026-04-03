import { CommonModule } from '@angular/common';
import { Component, Input, OnInit } from '@angular/core';
import {
  FormBuilder,
  FormGroup,
  FormArray,
  Validators,
  ReactiveFormsModule,
} from '@angular/forms';
import { TaskItem } from '../../../admin/models/taskitem';

@Component({
  selector: 'app-add-timesheet',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './add-timesheet.component.html',
  styleUrls: ['./add-timesheet.component.css'],
})
export class AddTimesheetComponent implements OnInit {
  timesheetForm!: FormGroup;

  @Input() taskitems: TaskItem[] = [];

  dailyMin = 8;
  dailyMax = 9;
  weeklyMin = 40;
  weeklyMax = 45;

  taskCodeMap: { [key: string]: { label: string; value: string }[] } = {
    work: [
      { label: 'API-1', value: 'API-1' },
      { label: 'API-2', value: 'API-2' },
      { label: 'UI-1', value: 'UI-1' },
      { label: 'UI-2', value: 'UI-2' },
      { label: 'Testing', value: 'Testing' },
      { label: 'Meeting', value: 'Meeting' },
      { label: 'Support', value: 'Support' },
    ],
    leave: [
      { label: 'Sick Leave - Full Day', value: 'sickleave-fullday' },
      { label: 'Sick Leave - Half Day', value: 'sickleave-halfday' },
      { label: 'Casual Leave - Full Day', value: 'casualleave-fullday' },
      { label: 'Casual Leave - Half Day', value: 'casualleave-halfday' },
      { label: 'Earned Leave - Full Day', value: 'earnedleave-fullday' },
      { label: 'Earned Leave - Half Day', value: 'earnedleave-halfday' },
      { label: 'Maternity Leave - Full Day', value: 'maternityleave-fullday' },
      { label: 'Maternity Leave - Half Day', value: 'maternityleave-halfday' },
      { label: 'Absent', value: 'absent' },
    ],
  };

  selectedDate: Date = new Date();
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
  showCalendar: boolean = false;
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

  weeks: Map<string, any[]> = new Map();
  currentWeekKey: string = '';
  availableWeeks: { key: string; label: string }[] = [];

  toastMessage: string = '';
  toastType: 'error' | 'warning' | 'success' = 'error';
  showToast: boolean = false;

  constructor(private fb: FormBuilder) {
    this.initializeWeekDates();
  }

  ngOnInit(): void {
    this.timesheetForm = this.fb.group({
      rows: this.fb.array([]),
    });

    this.currentWeekKey = this.getWeekKey(this.weekStart);
    this.updateAvailableWeeks();
    this.addRow();
  }

  // Toast
  showToastMessage(
    message: string,
    type: 'error' | 'warning' | 'success',
  ): void {
    this.toastMessage = message;
    this.toastType = type;
    this.showToast = true;
    setTimeout(() => this.hideToast(), 3000);
  }

  hideToast(): void {
    this.showToast = false;
    this.toastMessage = '';
  }

  // Date Helpers
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
    const day = date.getDate().toString().padStart(2, '0');
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    return `${day}/${month}/${date.getFullYear()}`;
  }

  formatDateForDisplay(date: Date): string {
    return `${this.monthNames[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;
  }

  // Week Management
  getWeekKey(date: Date): string {
    const year = date.getFullYear();
    const firstDayOfYear = new Date(year, 0, 1);
    const pastDays = (date.getTime() - firstDayOfYear.getTime()) / 86400000;
    const weekNumber = Math.ceil((pastDays + firstDayOfYear.getDay() + 1) / 7);
    return `${year}-W${weekNumber}`;
  }

  saveCurrentWeekData(): void {
    this.weeks.set(this.currentWeekKey, this.timesheetForm.getRawValue().rows);
    this.updateAvailableWeeks();
  }

  loadWeekData(event: any): void {
    this.saveCurrentWeekData();
    this.currentWeekKey = event.target.value;

    const weekData = this.weeks.get(this.currentWeekKey);

    while (this.rows.length) {
      this.rows.removeAt(0);
    }

    if (weekData && weekData.length > 0) {
      weekData.forEach((row: any) => {
        const newRow = this.createRow();
        newRow.patchValue(row);
        this.rows.push(newRow);
      });
    } else {
      this.addRow();
    }

    this.updateWeekDatesFromKey(this.currentWeekKey);
  }

  updateWeekDatesFromKey(weekKey: string): void {
    const [year, week] = weekKey.split('-W');
    const weekNumber = parseInt(week, 10);

    const firstDayOfYear = new Date(parseInt(year, 10), 0, 1);
    const startDate = new Date(firstDayOfYear);
    startDate.setDate(firstDayOfYear.getDate() + (weekNumber - 1) * 7);

    const dayOfWeek = startDate.getDay();
    const diffToMonday = dayOfWeek === 0 ? 6 : dayOfWeek - 1;

    this.weekStart = new Date(startDate);
    this.weekStart.setDate(startDate.getDate() - diffToMonday);

    this.updateWeekDates();
  }

  updateAvailableWeeks(): void {
    const allWeeks = new Set<string>();

    this.weeks.forEach((_, key) => allWeeks.add(key));
    if (this.currentWeekKey) allWeeks.add(this.currentWeekKey);

    this.availableWeeks = Array.from(allWeeks)
      .sort()
      .map((key) => ({
        key,
        label: this.formatWeekLabel(key),
      }));
  }

  formatWeekLabel(weekKey: string): string {
    const [year, week] = weekKey.split('-W');
    const weekNumber = parseInt(week, 10);

    const firstDayOfYear = new Date(parseInt(year, 10), 0, 1);
    const startDate = new Date(firstDayOfYear);
    startDate.setDate(firstDayOfYear.getDate() + (weekNumber - 1) * 7);

    const dayOfWeek = startDate.getDay();
    const diffToMonday = dayOfWeek === 0 ? 6 : dayOfWeek - 1;

    const weekStart = new Date(startDate);
    weekStart.setDate(startDate.getDate() - diffToMonday);

    const weekEnd = new Date(weekStart);
    weekEnd.setDate(weekStart.getDate() + 6);

    return `${this.formatDateForDisplay(weekStart)} - ${this.formatDateForDisplay(weekEnd)}`;
  }

  // Calendar
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
    this.currentWeekKey = this.getWeekKey(this.weekStart);
    this.loadWeekData({ target: { value: this.currentWeekKey } });
    this.showCalendar = false;
  }

  isCurrentMonth(date: Date): boolean {
    return (
      date.getMonth() === this.currentMonth.getMonth() &&
      date.getFullYear() === this.currentMonth.getFullYear()
    );
  }

  isSelectedWeek(date: Date): boolean {
    const d = new Date(date);
    d.setHours(0, 0, 0, 0);

    const start = new Date(this.weekStart);
    start.setHours(0, 0, 0, 0);

    const end = new Date(this.weekEnd);
    end.setHours(23, 59, 59, 999);

    return d >= start && d <= end;
  }

  // Form Array
  get rows(): FormArray {
    return this.timesheetForm.get('rows') as FormArray;
  }

  createRow(): FormGroup {
    return this.fb.group({
      taskItem: ['', Validators.required],
      taskCode: ['', Validators.required],
      monday: [0, [Validators.min(0), Validators.max(24)]],
      tuesday: [0, [Validators.min(0), Validators.max(24)]],
      wednesday: [0, [Validators.min(0), Validators.max(24)]],
      thursday: [0, [Validators.min(0), Validators.max(24)]],
      friday: [0, [Validators.min(0), Validators.max(24)]],
      saturday: [{ value: 0, disabled: true }],
      sunday: [{ value: 0, disabled: true }],
    });
  }

  addRow(): void {
    this.rows.push(this.createRow());
    this.showToastMessage('New row added', 'success');
  }

  removeRow(index: number): void {
    if (this.rows.length > 1) {
      this.rows.removeAt(index);
      this.showToastMessage('Row deleted successfully', 'success');
    }
  }

  getTaskCodes(taskItem: string) {
    return this.taskCodeMap[taskItem] || [];
  }

  onTaskItemChange(index: number) {
    this.rows.at(index).get('taskCode')?.setValue('');
  }

  getRowTotal(row: any): number {
    return [
      'monday',
      'tuesday',
      'wednesday',
      'thursday',
      'friday',
      'saturday',
      'sunday',
    ].reduce((sum, d) => sum + (Number(row[d]) || 0), 0);
  }

  getDayTotal(day: string): number {
    return this.rows.controls.reduce(
      (total, row) => total + (Number(row.getRawValue()[day]) || 0),
      0,
    );
  }

  getWorkedDayTotal(day: string): number {
    return this.rows.controls.reduce((total, row) => {
      const r = row.getRawValue();
      return total + (r.taskItem === 'work' ? Number(r[day]) || 0 : 0);
    }, 0);
  }

  getLeaveDayTotal(day: string): number {
    return this.rows.controls.reduce((total, row) => {
      const r = row.getRawValue();
      return total + (r.taskItem === 'leave' ? Number(r[day]) || 0 : 0);
    }, 0);
  }

  getWeekTotal(): number {
    return this.rows.controls.reduce(
      (total, row) => total + this.getRowTotal(row.getRawValue()),
      0,
    );
  }

  validateHourEntry(rowIndex: number, day: string, event: any): void {
    const value = parseFloat(event.target.value);

    if (isNaN(value)) {
      event.target.value = 0;
      this.rows.at(rowIndex).get(day)?.setValue(0);
      return;
    }

    const row = this.rows.at(rowIndex);
    const taskItem = row.get('taskItem')?.value;

    if (!taskItem) {
      this.showToastMessage('Please select Task Item first', 'error');
      event.target.value = 0;
      row.get(day)?.setValue(0);
      return;
    }

    row.get(day)?.setValue(value);
  }

  isDayComplete(day: string): boolean {
    const t = this.getDayTotal(day);
    return t >= this.dailyMin && t <= this.dailyMax;
  }

  isDayExceeded(day: string): boolean {
    return this.getDayTotal(day) > this.dailyMax;
  }

  isDayEditable(day: string): boolean {
    return !(day === 'saturday' || day === 'sunday');
  }

  getDayWarning(day: string): string {
    const total = this.getDayTotal(day);
    if (total > this.dailyMax) return `Exceeds ${this.dailyMax}h!`;
    if (total > 0 && total < this.dailyMin)
      return `Needs ${this.dailyMin - total}h more`;
    return '';
  }

  getDayCellClass(day: string): string {
    const t = this.getDayTotal(day);

    if (t > this.dailyMax) return 'cell-exceeded';
    if (t >= this.dailyMin && t <= this.dailyMax) return 'cell-completed';
    if (t > 0 && t < this.dailyMin) return 'cell-incomplete';

    return '';
  }

  isWeekValid(): boolean {
    const total = this.getWeekTotal();
    return total >= this.weeklyMin && total <= this.weeklyMax;
  }

  hasSubmitErrors(): boolean {
    return ['monday', 'tuesday', 'wednesday', 'thursday', 'friday'].some(
      (day) => this.isDayExceeded(day),
    );
  }

  submitTimesheet(): void {
    if (!this.isWeekValid()) {
      this.showToastMessage(
        `Weekly total (${this.getWeekTotal()}h) must be ${this.weeklyMin}-${this.weeklyMax}h.`,
        'error',
      );
      return;
    }

    if (this.timesheetForm.valid) {
      this.saveCurrentWeekData();
      this.showToastMessage(`Timesheet submitted!`, 'success');
      console.log('Submitted Data:', this.timesheetForm.getRawValue());
    } else {
      this.showToastMessage(
        'Fill all required fields (Task Item & Task Code)',
        'error',
      );
    }
  }
}
