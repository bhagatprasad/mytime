import { Component, Input, Output, OnChanges, SimpleChanges, EventEmitter } from '@angular/core';
import { Attendence } from '../../../admin/models/attendence';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-create-attendence',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule],
  templateUrl: 'create-attendence.html',
  styleUrl: 'create-attendence.css',
})

export class CreateAttendance implements OnChanges {

  @Input() isVisible: boolean = false;
  @Input() isCheckedIn: boolean = false;
  @Input() attendence: Attendence | null = null;
  @Input() isMobile: boolean = false;
  @Input() employeeId: number = 0;

  @Output() closeSidebar = new EventEmitter<void>();
  @Output() saveAttendance = new EventEmitter<Attendence>();


  attendanceForm: FormGroup;

  constructor(private fb: FormBuilder) {
    this.attendanceForm = this.fb.group({
      WorkType: [this.attendence?.Worktype || '', Validators.required],
      CheckInTime: [this.attendence?.CheckInTime || this.getCurrentISTTime(), Validators.required],
      CheckOutTime: [this.attendence?.CheckOutTime || ''],   // Will be filled on logout
      Description: [this.attendence?.Description || '']
    });
  }

  ngOnChanges(changes: SimpleChanges): void {

    if (changes['attendence']) {
      const attendence = changes['attendence'].currentValue;

      if (attendence) {
        // Patch all fields from the model
        this.attendanceForm.patchValue({
          WorkType: attendence.Worktype || '',
          Description: attendence.Description || '',
          CheckInTime: attendence.CheckInTime || this.getCurrentISTTime(),
          CheckOutTime: attendence.CheckOutTime || ''
        }, { emitEvent: false });

        // Mark form pristine/untouched if needed
        this.patchForm(attendence);

      } else if (!this.isVisible) {
        // If no attendence and sidebar is closed, reset form
        this.resetForm();
      }
    }
  }

  private patchForm(attendence: Attendence): void {
    // Only patch editable fields, don't emit value changes
    this.attendanceForm.patchValue(
      {
        WorkType: attendence.Worktype || '',
        Description: attendence.Description || ''
      },
      { emitEvent: false }
    );

    // Mark form as pristine after patching existing data
    if (attendence.EmployeeId) {
      this.attendanceForm.markAsPristine();
      this.attendanceForm.markAsUntouched();
    }
  }

  private resetForm(): void {
    this.attendanceForm.reset();
    this.attendanceForm.markAsPristine();
    this.attendanceForm.markAsUntouched();
  }

  ngOnInit(): void {
    // If document is provided on initialization, patch the form
    if (this.attendence) {
      this.patchForm(this.attendence);
    }
  }
  close(): void {
    this.resetForm();
    this.closeSidebar.emit();
  }
  onSubmit(): void {
    if (this.attendanceForm.valid) {

      const attendenceData: Attendence = {
        ...this.attendanceForm.value,
        EmployeeId: this.employeeId,
      };

      this.saveAttendance.emit(attendenceData);
      this.isCheckedIn = true;
      this.resetForm();

    } else {
      this.attendanceForm.markAllAsTouched();
    }
  }
  onLogout(): void {
    const logoutData: Attendence = {
      ...this.attendanceForm.value,
      EmployeeId: this.employeeId,
      CheckOutTime: this.getTodayDate()
    };
    this.saveAttendance.emit(logoutData);

    this.isCheckedIn = false;
    this.attendanceForm.reset();

  }
  private getTodayDate(): string {
    return new Date().toISOString().split('T')[0];
  }

  private getCurrentISTTime(): string {
    const now = new Date();

    return now.toLocaleTimeString('en-IN', {
      hour: '2-digit',
      minute: '2-digit',
      hour12: false, // 🔥 24-hour format
      timeZone: 'Asia/Kolkata' // 🔥 IST timezone
    });
  }
}