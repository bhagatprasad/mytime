import { Component, Input, Output, OnChanges, SimpleChanges, EventEmitter, OnInit, ElementRef, ViewChild } from '@angular/core';
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
  @Input() attendence: Attendence | null = null;
  @Input() isMobile: boolean = false;
  @Input() employeeId: number = 0;

  @Output() closeSidebar = new EventEmitter<void>();
  @Output() saveAttendance = new EventEmitter<Attendence>();

  attendanceForm: FormGroup;
  maxDate: string;
  minDate: string;
  isEditMode: boolean = false;

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
      CheckInTime: [this.attendence?.CheckInTime || this.getCurrentISTTime(), [
        Validators.required,
        this.timeFormatValidator.bind(this)
      ]],
      CheckOutTime: [this.attendence?.CheckOutTime || '', this.timeFormatValidator.bind(this)],
      Description: [this.attendence?.Description || '']
    });
  }

  ngOnInit(): void {
    if (this.attendence) {
      this.isEditMode = true;
      this.patchForm(this.attendence);
    }
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['attendence']) {
      const attendence = changes['attendence'].currentValue;

      if (attendence) {
        this.isEditMode = true;
        this.attendanceForm.patchValue({
          AttendanceDate: attendence.AttendenceDate || this.getTodayDate(),
          WorkType: attendence.WorkType || '',
          Description: attendence.Description || '',
          CheckInTime: attendence.CheckInTime || this.getCurrentISTTime(),
          CheckOutTime: attendence.CheckOutTime || ''
        }, { emitEvent: false });

        this.patchForm(attendence);

      } else if (!this.isVisible) {
        this.isEditMode = false;
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

  timeFormatValidator(control: AbstractControl): ValidationErrors | null {
    if (!control.value) {
      return null;
    }

    // Check if time is in HH:MM format (24-hour)
    const timeRegex = /^([0-1][0-9]|2[0-3]):[0-5][0-9]$/;
    if (!timeRegex.test(control.value)) {
      return { invalidTimeFormat: true };
    }

    return null;
  }

  validateTimeFormat(fieldName: string): void {
    const control = this.attendanceForm.get(fieldName);
    if (control && control.value) {
      const timeRegex = /^([0-1][0-9]|2[0-3]):[0-5][0-9]$/;
      if (!timeRegex.test(control.value)) {
        control.setErrors({ invalidTimeFormat: true });
      }
    }
  }

  openTimePicker(fieldName: string): void {
    // Create a temporary time input to use the native picker
    const tempInput = document.createElement('input');
    tempInput.type = 'time';
    tempInput.step = '60';

    // Set current value if exists
    const currentValue = this.attendanceForm.get(fieldName)?.value;
    if (currentValue) {
      tempInput.value = currentValue;
    }

    tempInput.addEventListener('change', (event: any) => {
      const selectedTime = event.target.value;
      if (selectedTime) {
        this.attendanceForm.patchValue({ [fieldName]: selectedTime });
        this.validateTimeFormat(fieldName);
      }
    });

    tempInput.click();
  }

  private patchForm(attendence: Attendence): void {
    this.attendanceForm.patchValue(
      {
        AttendanceDate: attendence.AttendenceDate || this.getTodayDate(),
        WorkType: attendence.WorkType || '',
        Description: attendence.Description || '',
        CheckInTime: attendence.CheckInTime || this.getCurrentISTTime(),
        CheckOutTime: attendence.CheckOutTime || ''
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
    this.isEditMode = false;
    this.resetForm();
    this.closeSidebar.emit();
  }

  onSubmit(): void {
    if (this.attendanceForm.valid) {
      const checkInTime = this.attendanceForm.value["CheckInTime"];
      const attendanceDate = this.attendanceForm.value["AttendanceDate"];

      let checkOutTime = this.attendanceForm.value["CheckOutTime"];
      let workHours = "";
      let status = "";

      // Handle Check-In/Logout logic
      if (this.attendence?.AttendenceId) {
        // This is a LOGOUT operation
        checkOutTime = this.getCurrentISTTime();
        status = "Logged Out";

        // Calculate work hours if both times exist
        if (checkInTime && checkOutTime) {
          workHours = this.getTimeDuration(checkInTime, checkOutTime);
        }
      } else {
        // This is a CHECK-IN operation
        status = "Logged Inn";
        workHours = "0h";
      }

      const attendenceData: Attendence = {
        AttendenceId: this.attendence?.AttendenceId ? this.attendence.AttendenceId : 0,
        EmployeeId: this.employeeId,
        AttendenceDate: attendanceDate ? new Date(attendanceDate) : new Date(),
        CheckInTime: checkInTime ? checkInTime : "",
        CheckOutTime: checkOutTime ? checkOutTime : "",
        Status: status,
        WorkHours: workHours,
        Description: this.attendanceForm.value["Description"],
        ApprovalStatus: this.attendence?.AttendenceId ? this.attendence.ApprovalStatus : "Pending",
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
      this.isEditMode = false;
      this.resetForm();
    } else {
      this.attendanceForm.markAllAsTouched();
    }
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
    console.log('Input times:', { checkingTime, checkOutTime });

    if (!checkingTime || !checkOutTime) {
      return "00:00";
    }

    const [checkinHours, checkinMinutes] = checkingTime.split(':').map(Number);
    const [checkoutHours, checkoutMinutes] = checkOutTime.split(':').map(Number);

    console.log('Parsed hours/minutes:', {
      checkinHours, checkinMinutes,
      checkoutHours, checkoutMinutes
    });

    const checkinTotalMinutes = (checkinHours * 60) + checkinMinutes;
    const checkoutTotalMinutes = (checkoutHours * 60) + checkoutMinutes;

    console.log('Total minutes:', { checkinTotalMinutes, checkoutTotalMinutes });

    let durationInMinutes;

    // Check if checkout time is on the next day
    if (checkoutTotalMinutes < checkinTotalMinutes) {
      console.log('Overnight shift detected');
      durationInMinutes = (checkoutTotalMinutes + 1440) - checkinTotalMinutes;
    } else {
      console.log('Same day shift');
      durationInMinutes = checkoutTotalMinutes - checkinTotalMinutes;
    }

    console.log('Duration in minutes:', durationInMinutes);

    const hours = Math.floor(durationInMinutes / 60);
    const minutes = durationInMinutes % 60;

    const result = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}`;
    console.log('Result:', result);

    return result;
  }
}