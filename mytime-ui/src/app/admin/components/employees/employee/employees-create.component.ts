import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, OnChanges, OnInit, Output, SimpleChanges } from '@angular/core';
import { FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { Employee } from '../../../models/employee';
import { Department } from '../../../models/department';
import { Role } from '../../../models/role';
import { Designation } from '../../../models/designation';

@Component({
  selector: 'app-employees-create',
  standalone: true,
  imports: [FormsModule, CommonModule, ReactiveFormsModule],
  templateUrl: './employees-create.component.html',
  styleUrl: './employees-create.component.css'
})
export class EmployeesCreateComponent implements OnInit, OnChanges {
  @Input() isVisible = false;
  @Input() employee: Employee | null = null;
  @Input() departments: Department[] = [];
  @Input() roles: Role[] = [];
  @Input() designations: Designation[] = [];

  @Output() saveEmployee = new EventEmitter<Employee>();
  @Output() closeSidebar = new EventEmitter<void>();

  employeeForm!: FormGroup;
  isCreateMode = false;

  constructor(private fb: FormBuilder) { }

  ngOnInit(): void {
    this.buildForm();
  }

  ngOnChanges(changes: SimpleChanges): void {
    console.log('ngOnChanges triggered:', changes);
    
    // Always reinitialize when isVisible changes to true
    if (changes['isVisible'] && changes['isVisible'].currentValue === true) {
      console.log('Sidebar opened. Employee:', this.employee);
      this.initializeForm();
    }
    
    // Also handle employee changes when sidebar is already visible
    if (changes['employee'] && this.isVisible) {
      console.log('Employee data updated:', this.employee);
      this.initializeForm();
    }
  }

  private initializeForm(): void {
    console.log('Initializing form. isVisible:', this.isVisible, 'employee:', this.employee);
    
    if (!this.isVisible) {
      console.log('Sidebar not visible, skipping initialization');
      return;
    }

    // Use setTimeout to ensure form is ready
    setTimeout(() => {
      this.isCreateMode = !this.employee;

      if (this.employee) {
        console.log('EDIT MODE - Patching form with:', this.employee);
        this.patchForm(this.employee);
      } else {
        console.log('CREATE MODE - Resetting form');
        this.resetForm();
        this.generateEmployeeCode();
      }
    });
  }

  private buildForm(): void {
    console.log('Building form');
    this.employeeForm = this.fb.group({
      EmployeeId: [0],
      EmployeeCode: ['', [Validators.required, Validators.maxLength(50)]],
      FirstName: ['', [Validators.required, Validators.maxLength(100)]],
      LastName: ['', Validators.maxLength(100)],
      FatherName: ['', Validators.maxLength(100)],
      MotherName: ['', Validators.maxLength(100)],
      Gender: [''],
      DateOfBirth: [''],
      Email: ['', [Validators.email, Validators.maxLength(100)]],
      Phone: ['', Validators.maxLength(20)],
      DepartmentId: [null, Validators.required],
      RoleId: [null, Validators.required],
      DesignationId: [null, Validators.required],
      StartedOn: [''],
      EndedOn: [''],
      ResignedOn: [''],
      LastWorkingDay: [''],
      OfferRelesedOn: [''],
      OfferAcceptedOn: [''],
      OfferPrice: [null],
      CurrentPrice: [null],
      JoiningBonus: [null],
      UserId: [null],
      IsActive: [true]
    });

    // Log when form is built
    console.log('Form built. Current value:', this.employeeForm.value);
  }

  private generateEmployeeCode(): void {
    if (!this.isCreateMode) return;

    const now = new Date();
    const datePart = this.formatDateForCode(now);
    const uniqueId = Math.floor(1000 + Math.random() * 9000);
    const employeeCode = `EMP${datePart}${uniqueId}_FS`;

    this.employeeForm.patchValue({
      EmployeeCode: employeeCode
    });
    
    console.log('Generated employee code:', employeeCode);
  }

  private formatDateForCode(date: Date): string {
    const year = date.getFullYear();
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    const day = date.getDate().toString().padStart(2, '0');
    return `${year}${month}${day}`;
  }

  private patchForm(employee: Employee): void {
    if (!employee) {
      console.error('Cannot patch form: employee is null or undefined');
      return;
    }

    console.log('=== PATCHING FORM ===');
    console.log('Employee object:', employee);
    console.log('Employee type:', typeof employee);

    // Check if employee is actually an object
    if (typeof employee !== 'object') {
      console.error('Employee is not an object:', employee);
      return;
    }

    // Check if form exists
    if (!this.employeeForm) {
      console.error('Form not initialized yet');
      return;
    }

    // Convert dates to proper format
    const formatDate = (dateValue: any): string => {
      if (!dateValue) return '';

      try {
        const date = new Date(dateValue);
        if (isNaN(date.getTime())) {
          console.warn('Invalid date value:', dateValue);
          return '';
        }
        return date.toISOString().split('T')[0];
      } catch (error) {
        console.warn('Error formatting date:', dateValue, error);
        return '';
      }
    };

    // Prepare form data with fallback values
    const formData = {
      EmployeeId: employee.EmployeeId || 0,
      EmployeeCode: employee.EmployeeCode || '',
      FirstName: employee.FirstName || '',
      LastName: employee.LastName || '',
      FatherName: employee.FatherName || '',
      MotherName: employee.MotherName || '',
      Gender: employee.Gender || '',
      DateOfBirth: formatDate(employee.DateOfBirth),
      Email: employee.Email || '',
      Phone: employee.Phone || '',
      DepartmentId: employee.DepartmentId ?? null,
      RoleId: employee.RoleId ?? null,
      DesignationId: employee.DesignationId ?? null,
      StartedOn: formatDate(employee.StartedOn),
      EndedOn: formatDate(employee.EndedOn),
      ResignedOn: formatDate(employee.ResignedOn),
      LastWorkingDay: formatDate(employee.LastWorkingDay),
      OfferRelesedOn: formatDate(employee.OfferRelesedOn),
      OfferAcceptedOn: formatDate(employee.OfferAcceptedOn),
      OfferPrice: employee.OfferPrice ?? null,
      CurrentPrice: employee.CurrentPrice ?? null,
      JoiningBonus: employee.JoiningBonus ?? null,
      UserId: employee.UserId ?? null,
      IsActive: employee.IsActive ?? true
    };

    console.log('Form data to patch:', formData);

    try {
      // First reset the form to clear any previous values
      this.employeeForm.reset();
      
      // Then patch the values
      this.employeeForm.patchValue(formData);
      
      console.log('Form successfully patched');
      console.log('Current form value:', this.employeeForm.value);
      
      // Force form validation update
      this.employeeForm.updateValueAndValidity();
    } catch (error) {
      console.error('Error patching form:', error);
    }
  }

  onSubmit(): void {
    if (this.employeeForm.invalid) {
      console.log('Form is invalid. Errors:', this.employeeForm.errors);
      this.employeeForm.markAllAsTouched();
      return;
    }

    const formValue = this.employeeForm.value;
    console.log('Submitting form:', formValue);

    const payload: Employee = {
      ...(this.employee || {}),
      ...formValue,
      OfferPrice: formValue.OfferPrice ? Number(formValue.OfferPrice) : null,
      CurrentPrice: formValue.CurrentPrice ? Number(formValue.CurrentPrice) : null,
      JoiningBonus: formValue.JoiningBonus ? Number(formValue.JoiningBonus) : null
    };

    this.saveEmployee.emit(payload);
  }

  close(): void {
    console.log('Closing sidebar');
    this.resetForm();
    this.closeSidebar.emit();
  }

  private resetForm(): void {
    console.log('Resetting form');
    
    this.employeeForm.reset({
      EmployeeId: 0,
      EmployeeCode: '',
      FirstName: '',
      LastName: '',
      FatherName: '',
      MotherName: '',
      Gender: '',
      DateOfBirth: '',
      Email: '',
      Phone: '',
      DepartmentId: null,
      RoleId: null,
      DesignationId: null,
      StartedOn: '',
      EndedOn: '',
      ResignedOn: '',
      LastWorkingDay: '',
      OfferRelesedOn: '',
      OfferAcceptedOn: '',
      OfferPrice: null,
      CurrentPrice: null,
      JoiningBonus: null,
      UserId: null,
      IsActive: true
    });

    this.employeeForm.markAsPristine();
    this.employeeForm.markAsUntouched();
    console.log('Form reset completed');
  }
}