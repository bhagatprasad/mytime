import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, OnChanges, Output, SimpleChanges } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { EmployeeEmergencyContact } from '../../../models/employee_emergency_contact';
import { LoaderService } from '../../../../common/services/loader.service';

@Component({
  selector: 'app-employees-emergency-contact-add',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './employees-emergencey-contact-add.component.html',
  styleUrl: './employees-emergencey-contact-add.component.css'
})
export class EmployeesEmergencyContactAddComponent implements OnChanges {
  @Input() employeeEmergencyContact: EmployeeEmergencyContact | null = null;
  @Input() isVisible: boolean = false;
  @Input() employeeId: number = 0;

  @Output() save = new EventEmitter<EmployeeEmergencyContact>();
  @Output() close = new EventEmitter<void>();

  contactForm: FormGroup;

  constructor(private fb: FormBuilder, private loader: LoaderService) {
    this.contactForm = this.fb.group({
      EmployeeEmergencyContactId: [0],
      EmployeeId: [this.employeeId],
      Name: ['', Validators.required],
      Relation: ['', Validators.required],
      Phone: ['', [Validators.required, Validators.pattern('^[0-9+\-\s()]+$')]],
      Email: ['', [Validators.email]],
      Address: [''],
      IsActive: [true]
    });
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['employeeEmergencyContact'] && this.employeeEmergencyContact) {
      this.initializeForm();
    }
    if (changes['employeeId'] && this.employeeId) {
      this.contactForm.patchValue({
        EmployeeId: this.employeeId
      });
    }
    if (changes['isVisible'] && this.isVisible && !this.employeeEmergencyContact) {
      this.resetForm();
    }
  }

  private initializeForm(): void {
    if (this.employeeEmergencyContact) {
      this.contactForm.patchValue({
        EmployeeEmergencyContactId: this.employeeEmergencyContact.EmployeeEmergencyContactId || 0,
        EmployeeId: this.employeeEmergencyContact.EmployeeId || this.employeeId,
        Name: this.employeeEmergencyContact.Name || '',
        Relation: this.employeeEmergencyContact.Relation || '',
        Phone: this.employeeEmergencyContact.Phone || '',
        Email: this.employeeEmergencyContact.Email || '',
        Address: this.employeeEmergencyContact.Address || '',
        IsActive: this.employeeEmergencyContact.IsActive !== undefined ? this.employeeEmergencyContact.IsActive : true
      });
    }
  }

  private resetForm(): void {
    this.contactForm.reset({
      EmployeeEmergencyContactId: 0,
      EmployeeId: this.employeeId,
      Name: '',
      Relation: '',
      Phone: '',
      Email: '',
      Address: '',
      IsActive: true
    });
  }

  onSubmit(): void {
    if (this.contactForm.valid) {
      const formValue = this.contactForm.value;
      
      const contactData: EmployeeEmergencyContact = {
        EmployeeEmergencyContactId: formValue.EmployeeEmergencyContactId || 0,
        EmployeeId: formValue.EmployeeId || this.employeeId,
        Name: formValue.Name,
        Relation: formValue.Relation,
        Phone: formValue.Phone,
        Email: formValue.Email || null,
        Address: formValue.Address || null,
        IsActive: formValue.IsActive,
        // Optional audit fields if needed
        CreatedOn: this.employeeEmergencyContact ? undefined : new Date().toISOString(),
        ModifiedOn: new Date().toISOString()
      };

      console.log('Sending emergency contact data:', contactData);
      this.save.emit(contactData);
    } else {
      Object.keys(this.contactForm.controls).forEach(key => {
        this.contactForm.get(key)?.markAsTouched();
      });
    }
  }

  onClose(): void {
    this.contactForm.reset();
    this.close.emit();
  }

  isFieldInvalid(fieldName: string): boolean {
    const field = this.contactForm.get(fieldName);
    return field ? (field.invalid && (field.dirty || field.touched)) : false;
  }

  getErrorMessage(fieldName: string): string {
    const field = this.contactForm.get(fieldName);
    if (field?.hasError('required')) {
      return `${this.getFieldLabel(fieldName)} is required`;
    }
    if (field?.hasError('email')) {
      return 'Please enter a valid email address';
    }
    if (field?.hasError('pattern')) {
      if (fieldName === 'Phone') {
        return 'Please enter a valid phone number';
      }
    }
    return '';
  }

  private getFieldLabel(fieldName: string): string {
    const labels: { [key: string]: string } = {
      Name: 'Name',
      Relation: 'Relationship',
      Phone: 'Phone number',
      Email: 'Email address',
      Address: 'Address'
    };
    return labels[fieldName] || fieldName;
  }
}