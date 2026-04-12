import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, OnChanges, Output, SimpleChanges } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { EmployeeEmployment } from '../../../models/employee_employment';
import { LoaderService } from '../../../../common/services/loader.service';

@Component({
  selector: 'app-employees-employement-add',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './employees-employement-add.component.html',
  styleUrl: './employees-employement-add.component.css'
})
export class EmployeesEmployementAddComponent implements OnChanges {
  @Input() employment: EmployeeEmployment | null = null;
  @Input() isVisible: boolean = false;
  @Input() employeeId: number = 0;

  @Output() save = new EventEmitter<EmployeeEmployment>();
  @Output() close = new EventEmitter<void>();

  employmentForm: FormGroup;

  constructor(private fb: FormBuilder, private loader: LoaderService) {
    this.employmentForm = this.fb.group({
      EmployeeEmploymentId: [0],
      EmployeeId: [this.employeeId],
      CompanyName: ['', Validators.required],
      Designation: ['', Validators.required],
      Address: ['', Validators.required],
      StartedOn: ['', Validators.required],
      EndedOn: [''],
      Reason: [''],
      ReportingManager: ['', Validators.required],
      HREmail: ['', [Validators.required, Validators.email]],
      Referance: [''],
      IsActive: [true]
    });
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['employment'] && this.employment) {
      this.initializeForm();
    }
    if (changes['employeeId'] && this.employeeId) {
      this.employmentForm.patchValue({
        EmployeeId: this.employeeId
      });
    }
    if (changes['isVisible'] && this.isVisible && !this.employment) {
      this.resetForm();
    }
  }

  private initializeForm(): void {
    if (this.employment) {
      // Format dates for input fields (yyyy-MM-dd)
      const formatDateForInput = (dateString: string | null | undefined): string => {
        if (!dateString) return '';
        // If it's already in YYYY-MM-DD format, return as is
        if (/^\d{4}-\d{2}-\d{2}$/.test(dateString)) {
          return dateString;
        }
        // Try to parse and format
        const date = new Date(dateString);
        if (isNaN(date.getTime())) return '';
        return date.toISOString().split('T')[0];
      };

      this.employmentForm.patchValue({
        EmployeeEmploymentId: this.employment.EmployeeEmploymentId || 0,
        EmployeeId: this.employment.EmployeeId || this.employeeId,
        CompanyName: this.employment.CompanyName || '',
        Designation: this.employment.Designation || '',
        Address: this.employment.Address || '',
        StartedOn: formatDateForInput(this.employment.StartedOn),
        EndedOn: formatDateForInput(this.employment.EndedOn),
        Reason: this.employment.Reason || '',
        ReportingManager: this.employment.ReportingManager || '',
        HREmail: this.employment.HREmail || '',
        Referance: this.employment.Referance || '',
        IsActive: this.employment.IsActive !== undefined ? this.employment.IsActive : true
      });
    }
  }

  private resetForm(): void {
    this.employmentForm.reset({
      EmployeeEmploymentId: 0,
      EmployeeId: this.employeeId,
      CompanyName: '',
      Designation: '',
      Address: '',
      StartedOn: '',
      EndedOn: '',
      Reason: '',
      ReportingManager: '',
      HREmail: '',
      Referance: '',
      IsActive: true
    });
  }

  /**
   * Convert date string to datetimeoffset format
   * @param dateStr - Date string in YYYY-MM-DD format
   * @returns ISO datetime string with timezone or null
   */
  private convertToDateTimeOffset(dateStr: string | null): string | null {
    if (!dateStr) return null;

    try {
      // Create date at start of day in local timezone
      const date = new Date(dateStr);
      date.setHours(0, 0, 0, 0);

      // Get timezone offset in minutes and convert to +/-HH:MM format
      const offset = -date.getTimezoneOffset();
      const offsetHours = Math.floor(Math.abs(offset) / 60);
      const offsetMinutes = Math.abs(offset) % 60;
      const offsetSign = offset >= 0 ? '+' : '-';
      const timezoneOffset = `${offsetSign}${offsetHours.toString().padStart(2, '0')}:${offsetMinutes.toString().padStart(2, '0')}`;

      // Format: YYYY-MM-DDTHH:MM:SS+HH:MM
      const year = date.getFullYear();
      const month = (date.getMonth() + 1).toString().padStart(2, '0');
      const day = date.getDate().toString().padStart(2, '0');

      return `${year}-${month}-${day}T00:00:00${timezoneOffset}`;
    } catch (error) {
      console.error('Error converting date to datetimeoffset:', error);
      return null;
    }
  }

  onSubmit(): void {
    if (this.employmentForm.valid) {
      const formValue = this.employmentForm.value;
      // Convert dates to datetimeoffset format
      const startedOn = this.convertToDateTimeOffset(formValue.StartedOn);
      const endedOn = this.convertToDateTimeOffset(formValue.EndedOn);

      // Get current datetime in datetimeoffset format for audit fields
      const now = new Date();
      const currentDateTime = this.convertToDateTimeOffset(now.toISOString().split('T')[0]) || now.toISOString();

      const employmentData: EmployeeEmployment = {
        EmployeeEmploymentId: formValue.EmployeeEmploymentId || 0,
        EmployeeId: formValue.EmployeeId || this.employeeId,
        CompanyName: formValue.CompanyName,
        Designation: formValue.Designation,
        Address: formValue.Address,
        StartedOn: startedOn,  // Now in datetimeoffset format: "2024-02-12T00:00:00+05:30"
        EndedOn: endedOn,      // Now in datetimeoffset format or null
        Reason: formValue.Reason || null,
        ReportingManager: formValue.ReportingManager,
        HREmail: formValue.HREmail,
        Referance: formValue.Referance || null,
        IsActive: formValue.IsActive,
        // Add audit fields if needed
        CreatedOn: this.employment ? undefined : currentDateTime,
        ModifiedOn: currentDateTime
      };

      console.log('Sending employment data:', employmentData);
      this.save.emit(employmentData);
    } else {
      Object.keys(this.employmentForm.controls).forEach(key => {
        this.employmentForm.get(key)?.markAsTouched();
      });
    }
  }

  onClose(): void {
    this.employmentForm.reset();
    this.close.emit();
  }

  isFieldInvalid(fieldName: string): boolean {
    const field = this.employmentForm.get(fieldName);
    return field ? (field.invalid && (field.dirty || field.touched)) : false;
  }

  getErrorMessage(fieldName: string): string {
    const field = this.employmentForm.get(fieldName);
    if (field?.hasError('required')) {
      return `${this.getFieldLabel(fieldName)} is required`;
    }
    if (field?.hasError('email')) {
      return 'Please enter a valid email address';
    }
    return '';
  }

  private getFieldLabel(fieldName: string): string {
    const labels: { [key: string]: string } = {
      CompanyName: 'Company name',
      Designation: 'Designation',
      Address: 'Address',
      StartedOn: 'Start date',
      ReportingManager: 'Reporting manager',
      HREmail: 'HR email'
    };
    return labels[fieldName] || fieldName;
  }

  validateDateRange(): boolean {
    const startedOn = this.employmentForm.get('StartedOn')?.value;
    const endedOn = this.employmentForm.get('EndedOn')?.value;

    if (startedOn && endedOn) {
      return new Date(endedOn) >= new Date(startedOn);
    }
    return true;
  }
}