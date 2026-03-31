import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import {
  FormBuilder,
  FormGroup,
  FormArray,
  Validators,
  ReactiveFormsModule,
} from '@angular/forms';

@Component({
  selector: 'app-add-timesheet',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './add-timesheet.component.html',
  styleUrls: ['./add-timesheet.component.css'],
})
export class AddTimesheetComponent implements OnInit {
  timesheetForm!: FormGroup;

  // Company rules
  dailyMin = 8;
  dailyMax = 9;
  weeklyMin = 40;
  weeklyMax = 45;

  // Task Items
  taskItems: string[] = ['work', 'leave'];

  // Task Codes
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

  // Date range properties
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

  // Calendar view properties
  currentMonth: Date = new Date();
  currentYear: number = new Date().getFullYear();
  calendarDays: Date[] = [];
  showCalendar: boolean = false;

  // View modes
  viewMode: 'week' | 'month' | 'year' = 'week';

  // Month names
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

  // Multi-week storage
  weeks: Map<string, any[]> = new Map();
  currentWeekKey: string = '';
  availableWeeks: { key: string; label: string }[] = [];

  // Toast message properties
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

  // Toast notification methods
  showToastMessage(
    message: string,
    type: 'error' | 'warning' | 'success',
  ): void {
    this.toastMessage = message;
    this.toastType = type;
    this.showToast = true;

    setTimeout(() => {
      this.hideToast();
    }, 3000);
  }

  hideToast(): void {
    this.showToast = false;
    this.toastMessage = '';
  }

  // Date methods
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
    const year = date.getFullYear();
    return `${day}/${month}/${year}`;
  }

  formatDateForDisplay(date: Date): string {
    const day = date.getDate();
    const month = this.monthNames[date.getMonth()];
    const year = date.getFullYear();
    return `${month} ${day}, ${year}`;
  }

  // Week management methods
  getWeekKey(date: Date): string {
    const year = date.getFullYear();
    const weekNumber = this.getWeekNumber(date);
    return `${year}-W${weekNumber}`;
  }

  getWeekNumber(date: Date): number {
    const firstDayOfYear = new Date(date.getFullYear(), 0, 1);
    const pastDaysOfYear =
      (date.getTime() - firstDayOfYear.getTime()) / 86400000;
    return Math.ceil((pastDaysOfYear + firstDayOfYear.getDay() + 1) / 7);
  }

  saveCurrentWeekData(): void {
    const currentData = this.timesheetForm.getRawValue();
    this.weeks.set(this.currentWeekKey, currentData.rows);
    this.updateAvailableWeeks();
  }

  loadWeekData(event: any): void {
    const weekKey = event.target.value;
    this.saveCurrentWeekData();

    this.currentWeekKey = weekKey;
    const weekData = this.weeks.get(weekKey);

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

    this.updateWeekDatesFromKey(weekKey);
  }

  updateWeekDatesFromKey(weekKey: string): void {
    const [year, week] = weekKey.split('-W');
    const weekNumber = parseInt(week);

    const firstDayOfYear = new Date(parseInt(year), 0, 1);
    const daysOffset = (weekNumber - 1) * 7;
    const startDate = new Date(firstDayOfYear);
    startDate.setDate(firstDayOfYear.getDate() + daysOffset);

    const dayOfWeek = startDate.getDay();
    const diffToMonday = dayOfWeek === 0 ? 6 : dayOfWeek - 1;
    this.weekStart = new Date(startDate);
    this.weekStart.setDate(startDate.getDate() - diffToMonday);

    this.updateWeekDates();
  }

  updateAvailableWeeks(): void {
    const allWeeks = new Set<string>();

    this.weeks.forEach((_, key) => {
      allWeeks.add(key);
    });

    if (this.currentWeekKey) {
      allWeeks.add(this.currentWeekKey);
    }

    this.availableWeeks = Array.from(allWeeks)
      .sort((a, b) => a.localeCompare(b))
      .map((key) => ({
        key: key,
        label: this.formatWeekLabel(key),
      }));
  }

  formatWeekLabel(weekKey: string): string {
    const [year, week] = weekKey.split('-W');
    const weekNumber = parseInt(week);

    const firstDayOfYear = new Date(parseInt(year), 0, 1);
    const daysOffset = (weekNumber - 1) * 7;
    const startDate = new Date(firstDayOfYear);
    startDate.setDate(firstDayOfYear.getDate() + daysOffset);

    const dayOfWeek = startDate.getDay();
    const diffToMonday = dayOfWeek === 0 ? 6 : dayOfWeek - 1;
    const weekStart = new Date(startDate);
    weekStart.setDate(startDate.getDate() - diffToMonday);

    const weekEnd = new Date(weekStart);
    weekEnd.setDate(weekStart.getDate() + 6);

    return `${this.formatDateForDisplay(weekStart)} - ${this.formatDateForDisplay(weekEnd)}`;
  }

  goToPreviousWeek(): void {
    this.saveCurrentWeekData();
    const prevWeek = new Date(this.weekStart);
    prevWeek.setDate(this.weekStart.getDate() - 7);
    this.weekStart = prevWeek;
    this.updateWeekDates();
    this.currentWeekKey = this.getWeekKey(this.weekStart);
    this.loadWeekData({ target: { value: this.currentWeekKey } });
  }

  goToNextWeek(): void {
    this.saveCurrentWeekData();
    const nextWeek = new Date(this.weekStart);
    nextWeek.setDate(this.weekStart.getDate() + 7);
    this.weekStart = nextWeek;
    this.updateWeekDates();
    this.currentWeekKey = this.getWeekKey(this.weekStart);

    const weekData = this.weeks.get(this.currentWeekKey);
    if (weekData) {
      this.loadWeekData({ target: { value: this.currentWeekKey } });
    } else {
      while (this.rows.length) {
        this.rows.removeAt(0);
      }
      this.addRow();
    }
  }

  goToToday(): void {
    this.saveCurrentWeekData();
    this.initializeWeekDates();
    this.currentWeekKey = this.getWeekKey(this.weekStart);
    this.loadWeekData({ target: { value: this.currentWeekKey } });
  }

  // Calendar methods
  toggleCalendar(): void {
    this.showCalendar = !this.showCalendar;
    if (this.showCalendar) {
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
    const startDayOfWeek = startDate.getDay();
    startDate.setDate(startDate.getDate() - startDayOfWeek);

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
    this.generateCalendarDays();
  }

  nextMonth(): void {
    this.currentMonth = new Date(
      this.currentYear,
      this.currentMonth.getMonth() + 1,
      1,
    );
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
    return date.getMonth() === this.currentMonth.getMonth();
  }

  isSelectedWeek(date: Date): boolean {
    const weekStartCopy = new Date(this.weekStart);
    const weekEndCopy = new Date(this.weekEnd);
    return date >= weekStartCopy && date <= weekEndCopy;
  }

  setViewMode(mode: 'week' | 'month' | 'year'): void {
    this.viewMode = mode;
  }

  // Form methods
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
  }

  removeRow(index: number): void {
    if (this.rows.length > 1) {
      const rowToRemove = this.rows.at(index);
      const rowData = rowToRemove.getRawValue();

      const affectedDays = [
        'monday',
        'tuesday',
        'wednesday',
        'thursday',
        'friday',
      ].filter((day) => Number(rowData[day] || 0) > 0);

      if (affectedDays.length > 0) {
        const confirmDelete = confirm(
          `This row has ${affectedDays.length} day(s) with hours. Removing it may make those days incomplete. Continue?`,
        );
        if (!confirmDelete) {
          return;
        }
      }

      this.rows.removeAt(index);
      affectedDays.forEach((day) => {
        this.validateDayAfterChange(day);
      });

      this.showToastMessage('Row deleted successfully', 'success');
    }
  }

  getTaskCodes(taskItem: string): { label: string; value: string }[] {
    return this.taskCodeMap[taskItem] || [];
  }

  onTaskItemChange(index: number): void {
    const row = this.rows.at(index);
    row.get('taskCode')?.setValue('');
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

  getWorkedDayTotal(day: string): number {
    return this.rows.controls.reduce((total, row) => {
      const rowValue = row.getRawValue();
      if (rowValue.taskItem === 'work') {
        return total + Number(rowValue[day] || 0);
      }
      return total;
    }, 0);
  }

  getLeaveDayTotal(day: string): number {
    return this.rows.controls.reduce((total, row) => {
      const rowValue = row.getRawValue();
      if (rowValue.taskItem === 'leave') {
        return total + Number(rowValue[day] || 0);
      }
      return total;
    }, 0);
  }

  getWorkedWeekTotal(): number {
    return this.rows.controls.reduce((total, row) => {
      const rowValue = row.getRawValue();
      if (rowValue.taskItem === 'work') {
        return total + this.getRowTotal(rowValue);
      }
      return total;
    }, 0);
  }

  getLeaveWeekTotal(): number {
    return this.rows.controls.reduce((total, row) => {
      const rowValue = row.getRawValue();
      if (rowValue.taskItem === 'leave') {
        return total + this.getRowTotal(rowValue);
      }
      return total;
    }, 0);
  }

  getWeekTotal(): number {
    return this.rows.controls.reduce((total, row) => {
      return total + this.getRowTotal(row.getRawValue());
    }, 0);
  }

  // Validation methods
  validateDayAfterChange(day: string): void {
    const total = this.getDayTotal(day);
    const worked = this.getWorkedDayTotal(day);
    const leave = this.getLeaveDayTotal(day);

    if (total > this.dailyMax) {
      this.showToastMessage(
        `${this.capitalize(day)} has exceeded ${this.dailyMax} hours! Current: ${total} hrs`,
        'error',
      );
    } else if (
      worked > 0 &&
      leave > 0 &&
      total >= this.dailyMin &&
      total <= this.dailyMax
    ) {
      this.showToastMessage(
        `${this.capitalize(day)}: ${worked}h work + ${leave}h leave = ${total}h (Half Day Work + Half Day Leave)`,
        'success',
      );
    } else if (total >= this.dailyMin && total <= this.dailyMax) {
      this.showToastMessage(
        `${this.capitalize(day)} completed with ${total} hours!`,
        'success',
      );
    } else if (total > 0 && total < this.dailyMin) {
      const remaining = this.dailyMin - total;
      this.showToastMessage(
        `${this.capitalize(day)} needs ${remaining} more hour(s) to reach minimum ${this.dailyMin} hrs`,
        'warning',
      );
    }
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

    const existingWork = this.getWorkedDayTotal(day);
    const existingLeave = this.getLeaveDayTotal(day);
    const oldValue = Number(row.get(day)?.value || 0);

    let newWorkValue = 0;
    let newLeaveValue = 0;

    if (taskItem === 'work') {
      newWorkValue = value;
      newLeaveValue = existingLeave;
    } else if (taskItem === 'leave') {
      newLeaveValue = value;
      newWorkValue = existingWork;
    }

    const totalAfterChange = newWorkValue + newLeaveValue;

    if (taskItem === 'work' && existingLeave > 0) {
      this.showToastMessage(
        `Cannot add work on ${this.capitalize(day)} because it already has ${existingLeave}h of leave.`,
        'error',
      );
      row.get(day)?.setValue(oldValue);
      event.target.value = oldValue;
      return;
    }

    if (taskItem === 'leave' && existingWork > 0) {
      this.showToastMessage(
        `Cannot add leave on ${this.capitalize(day)} because it already has ${existingWork}h of work.`,
        'error',
      );
      row.get(day)?.setValue(oldValue);
      event.target.value = oldValue;
      return;
    }

    if (totalAfterChange > this.dailyMax) {
      this.showToastMessage(
        `${this.capitalize(day)} cannot exceed ${this.dailyMax} hours. Current: ${existingWork + existingLeave}h`,
        'error',
      );
      row.get(day)?.setValue(oldValue);
      event.target.value = oldValue;
      return;
    }

    this.validateDayAfterChange(day);
  }

  isDayComplete(day: string): boolean {
    const total = this.getDayTotal(day);
    return total >= this.dailyMin && total <= this.dailyMax;
  }

  isDayExceeded(day: string): boolean {
    return this.getDayTotal(day) > this.dailyMax;
  }

  isDayEditable(day: string): boolean {
    if (day === 'saturday' || day === 'sunday') {
      return false;
    }

    if (this.isDayComplete(day)) {
      return false;
    }

    switch (day) {
      case 'monday':
        return true;
      case 'tuesday':
        return this.isDayComplete('monday');
      case 'wednesday':
        return this.isDayComplete('tuesday');
      case 'thursday':
        return this.isDayComplete('wednesday');
      case 'friday':
        return this.isDayComplete('thursday');
      default:
        return false;
    }
  }

  onDayFocus(day: string): void {
    if (!this.isDayEditable(day) && day !== 'saturday' && day !== 'sunday') {
      let message = '';
      if (this.isDayComplete(day)) {
        message = `${this.capitalize(day)} is already completed. You cannot edit it.`;
      } else if (day === 'tuesday' && !this.isDayComplete('monday')) {
        message = `Please complete Monday first before entering Tuesday.`;
      } else if (day === 'wednesday' && !this.isDayComplete('tuesday')) {
        message = `Please complete Tuesday first before entering Wednesday.`;
      } else if (day === 'thursday' && !this.isDayComplete('wednesday')) {
        message = `Please complete Wednesday first before entering Thursday.`;
      } else if (day === 'friday' && !this.isDayComplete('thursday')) {
        message = `Please complete Thursday first before entering Friday.`;
      }

      if (message) {
        this.showToastMessage(message, 'warning');
      }
    }
  }

  getDayWarning(day: string): string {
    const total = this.getDayTotal(day);
    const worked = this.getWorkedDayTotal(day);
    const leave = this.getLeaveDayTotal(day);

    if (total > this.dailyMax) {
      return `⚠️ Exceeds ${this.dailyMax}h limit!`;
    }
    if (total > 0 && total < this.dailyMin) {
      return `⚠️ Needs ${this.dailyMin - total}h more`;
    }
    if (worked > 0 && leave > 0) {
      return `✓ ${worked}h work + ${leave}h leave`;
    }
    return '';
  }

  getDayCellClass(day: string): string {
    const total = this.getDayTotal(day);
    if (total > this.dailyMax) return 'cell-exceeded';
    if (total >= this.dailyMin && total <= this.dailyMax)
      return 'cell-completed';
    if (total > 0 && total < this.dailyMin) return 'cell-incomplete';
    return '';
  }

  capitalize(day: string): string {
    return day.charAt(0).toUpperCase() + day.slice(1);
  }

  isWeekValid(): boolean {
    const total = this.getWeekTotal();
    return total >= this.weeklyMin && total <= this.weeklyMax;
  }

  getDayStatus(day: string): string {
    if (day === 'saturday' || day === 'sunday') {
      return 'Holiday';
    }

    const total = this.getDayTotal(day);
    const worked = this.getWorkedDayTotal(day);
    const leave = this.getLeaveDayTotal(day);

    if (total > this.dailyMax) {
      return 'Exceeded';
    }

    if (worked > 0 && leave > 0) {
      if (total >= this.dailyMin && total <= this.dailyMax) {
        return 'Half Leave + Work';
      }
      if (total < this.dailyMin) {
        return 'Incomplete';
      }
    }

    if (worked === 0 && leave >= this.dailyMin) {
      return 'Full Leave';
    }

    if (leave === 0 && worked >= this.dailyMin) {
      return 'Full Work';
    }

    if (total < this.dailyMin && total > 0) {
      return 'Incomplete';
    }

    if (total === 0) {
      return 'Incomplete';
    }

    return 'Valid';
  }

  getDayStatusShort(day: string): string {
    const status = this.getDayStatus(day);
    const worked = this.getWorkedDayTotal(day);
    const leave = this.getLeaveDayTotal(day);

    switch (status) {
      case 'Full Work':
        return '✓ Work';
      case 'Half Leave + Work':
        return `${worked}h + ${leave}h`;
      case 'Full Leave':
        return '✗ Leave';
      case 'Incomplete':
        return '⚠️ Inc';
      case 'Exceeded':
        return '⚠️ Exc';
      case 'Holiday':
        return 'Holiday';
      default:
        return '—';
    }
  }

  getDayBreakdown(day: string): string {
    const worked = this.getWorkedDayTotal(day);
    const leave = this.getLeaveDayTotal(day);
    const total = worked + leave;

    if (worked > 0 && leave > 0) {
      return `${worked}h + ${leave}h = ${total}h`;
    }
    if (worked > 0) {
      return `${worked}h Work`;
    }
    if (leave > 0) {
      return `${leave}h Leave`;
    }
    return '0h';
  }

  getDayStatusClass(day: string): string {
    const status = this.getDayStatus(day);
    switch (status) {
      case 'Full Work':
        return 'status-work';
      case 'Half Leave + Work':
        return 'status-half';
      case 'Full Leave':
        return 'status-leave';
      case 'Incomplete':
        return 'status-incomplete';
      case 'Exceeded':
        return 'status-exceeded';
      case 'Holiday':
        return 'status-holiday';
      default:
        return '';
    }
  }

  hasSubmitErrors(): boolean {
    return (
      this.isDayExceeded('monday') ||
      this.isDayExceeded('tuesday') ||
      this.isDayExceeded('wednesday') ||
      this.isDayExceeded('thursday') ||
      this.isDayExceeded('friday')
    );
  }

  submitTimesheet(): void {
    const exceededDays = [
      'monday',
      'tuesday',
      'wednesday',
      'thursday',
      'friday',
    ].filter((day) => this.isDayExceeded(day));

    if (exceededDays.length > 0) {
      this.showToastMessage(
        `Please correct exceeded hours for: ${exceededDays.map((d) => this.capitalize(d)).join(', ')}`,
        'error',
      );
      return;
    }

    if (!this.isWeekValid()) {
      this.showToastMessage(
        `Weekly total (${this.getWeekTotal()} hrs) should be between ${this.weeklyMin} and ${this.weeklyMax} hours.`,
        'error',
      );
      return;
    }

    if (this.timesheetForm.valid) {
      this.saveCurrentWeekData();
      this.showToastMessage(
        `Timesheet for week ${this.formatWeekLabel(this.currentWeekKey)} submitted successfully!`,
        'success',
      );
    } else {
      this.showToastMessage(
        'Please fill all required fields (Task Item and Task Code)',
        'error',
      );
    }
  }
}
