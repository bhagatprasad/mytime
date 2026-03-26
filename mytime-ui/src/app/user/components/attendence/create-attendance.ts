import { Component, Input, Output, OnChanges, SimpleChanges, EventEmitter, OnInit } from '@angular/core';
import { Attendence } from '../../../admin/models/attendence';
import { FormBuilder, FormGroup, Validators, AbstractControl, ValidationErrors } from '@angular/forms';
import { ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-create-attendence',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule],
  templateUrl: 'create-attendence.html',
  styleUrl: 'create-attendence.css',
})

export class CreateAttendance implements OnChanges, OnInit {

  @Input() isVisible: boolean = false;
  @Input() isCheckedIn: boolean = false;
  @Input() attendence: Attendence | null = null;
  @Input() isMobile: boolean = false;
  @Input() employeeId: number = 0;

  @Output() closeSidebar = new EventEmitter<void>();
  @Output() saveAttendance = new EventEmitter<Attendence>();

  attendanceForm: FormGroup;
  maxDate: string;
  minDate: string;

  constructor(private fb: FormBuilder) {
    const today = new Date();
    this.maxDate = this.formatDateForInput(today);
    const minDateObj = new Date(today);
    minDateObj.setDate(minDateObj.getDate() - 30); // Allow last 30 days
    this.minDate = this.formatDateForInput(minDateObj);

    this.attendanceForm = this.fb.group({
      AttendanceDate: [this.attendence?.AttendenceDate || this.getTodayDate(), [
        Validators.required,
        this.futureDateValidator.bind(this)
      ]],
      WorkType: [this.attendence?.WorkType || '', Validators.required],
      CheckInTime: [this.attendence?.CheckInTime || this.getCurrentISTTime(), Validators.required],
      CheckOutTime: [this.attendence?.CheckOutTime || ''],
      Description: [this.attendence?.Description || '']
    });
  }

  ngOnInit(): void {
    if (this.attendence) {
      this.patchForm(this.attendence);
    }
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['attendence']) {
      const attendence = changes['attendence'].currentValue;

      if (attendence) {
        this.attendanceForm.patchValue({
          AttendanceDate: attendence.AttendanceDate || this.getTodayDate(),
          WorkType: attendence.WorkType || '',
          Description: attendence.Description || '',
          CheckInTime: attendence.CheckInTime || this.getCurrentISTTime(),
          CheckOutTime: attendence.CheckOutTime || ''
        }, { emitEvent: false });

        this.patchForm(attendence);

      } else if (!this.isVisible) {
        this.resetForm();
      }
    }
  }

  futureDateValidator(control: AbstractControl): ValidationErrors | null {
    if (!control.value) {
      return null;
    }

    const selectedDate = new Date(control.value);
    const today = new Date();

    selectedDate.setHours(0, 0, 0, 0);
    today.setHours(0, 0, 0, 0);

    if (selectedDate > today) {
      return { futureDate: true };
    }

    return null;
  }

  private patchForm(attendence: Attendence): void {
    this.attendanceForm.patchValue(
      {
        AttendanceDate: attendence.AttendenceDate || this.getTodayDate(),
        WorkType: attendence.WorkType || '',
        Description: attendence.Description || ''
      },
      { emitEvent: false }
    );

    if (attendence.EmployeeId) {
      this.attendanceForm.markAsPristine();
      this.attendanceForm.markAsUntouched();
    }
  }

  private resetForm(): void {
    this.attendanceForm.reset({
      AttendanceDate: this.getTodayDate(),
      WorkType: '',
      CheckInTime: this.getCurrentISTTime(),
      CheckOutTime: '',
      Description: ''
    });
    this.attendanceForm.markAsPristine();
    this.attendanceForm.markAsUntouched();
  }

  close(): void {
    this.resetForm();
    this.closeSidebar.emit();
  }

  onSubmit(): void {
    if (this.attendanceForm.valid) {
        const checkInTime = this.attendanceForm.value["CheckInTime"];
        const checkOutTime = this.attendanceForm.value["CheckOutTime"];
        const attendanceDate = this.attendanceForm.value["AttendanceDate"];

        let workHours = "";
        if (checkInTime && checkOutTime) {
            workHours = this.getTimeDuration(checkInTime, checkOutTime);
        }
        
        const attendenceData: Attendence = {
            AttendenceId: this.attendence?.AttendenceId ? this.attendence.AttendenceId : 0,
            EmployeeId: this.employeeId,
            AttendenceDate: attendanceDate ? new Date(attendanceDate) : new Date(),
            CheckInTime: checkInTime ? checkInTime : "",
            CheckOutTime: checkOutTime ? checkOutTime : "",
            Status: this.attendence?.AttendenceId ? "Logged Out" : "Logged Inn",
            WorkHours: workHours,
            Description: this.attendanceForm.value["Description"],
            ApprovalStatus: this.attendence?.AttendenceId ? this.attendence.ApprovalStatus : "",
            ApprovedBy: this.attendence?.AttendenceId ? this.attendence.ApprovedBy : undefined,
            WorkType: this.attendanceForm.value["WorkType"],
            CreatedBy: this.attendence?.AttendenceId ? this.attendence.CreatedBy : undefined,
            CreatedOn: this.attendence?.AttendenceId ? this.attendence.CreatedOn : new Date(),
            ModifiedBy: this.attendence?.AttendenceId ? this.attendence.ModifiedBy : undefined,
            ModifiedOn: this.attendence?.AttendenceId ? new Date() : undefined,
            ApprovedOn: this.attendence?.AttendenceId ? this.attendence.ApprovedOn : undefined,
            RejectedBy: this.attendence?.AttendenceId ? this.attendence.RejectedBy : undefined,
            RejectedOn: this.attendence?.AttendenceId ? this.attendence.RejectedOn : undefined,
            RejectionReason: this.attendence?.AttendenceId ? this.attendence.RejectionReason : undefined
        };

        this.saveAttendance.emit(attendenceData);
        this.resetForm();
    } else {
        this.attendanceForm.markAllAsTouched();
    }
}

  onLogout(): void {
    const logoutData: Attendence = {
      ...this.attendanceForm.value,
      EmployeeId: this.employeeId,
      CheckOutTime: this.getCurrentISTTime()
    };
    this.saveAttendance.emit(logoutData);
    this.resetForm();
  }

  private getTodayDate(): string {
    return new Date().toISOString().split('T')[0];
  }

  private getCurrentISTTime(): string {
    const now = new Date();
    return now.toLocaleTimeString('en-IN', {
      hour: '2-digit',
      minute: '2-digit',
      hour12: false,
      timeZone: 'Asia/Kolkata'
    });
  }

  private formatDateForInput(date: Date): string {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  }

  getTimeDuration(checkingTime: string, checkOutTime: string): string {
    const [checkinHours, checkinMinutes] = checkingTime.split(':').map(Number);
    const [checkoutHours, checkoutMinutes] = checkOutTime.split(':').map(Number);

    const checkinTotalMinutes = (checkinHours * 60) + checkinMinutes;
    let checkoutTotalMinutes = (checkoutHours * 60) + checkoutMinutes;

    if (checkoutTotalMinutes <= checkinTotalMinutes) {
      checkoutTotalMinutes += 24 * 60;
    }

    const durationInMinutes = checkoutTotalMinutes - checkinTotalMinutes;

    const hours = Math.floor(durationInMinutes / 60);
    const minutes = durationInMinutes % 60;

    return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}`;
  }
}