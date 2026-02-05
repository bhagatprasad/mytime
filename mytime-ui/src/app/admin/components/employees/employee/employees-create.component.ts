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

  constructor(private fb: FormBuilder) {}

  ngOnInit(): void {
    this.buildForm();
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['isVisible']?.currentValue) {
      this.isCreateMode = !this.employee;
      
      if (this.employee) {
        // Edit mode - use existing employee code
        this.patchForm(this.employee);
      } else {
        // Create mode - reset form and generate new code
        this.resetForm();
        this.generateEmployeeCode();
      }
    }
  }

  private buildForm(): void {
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
  }

  private generateEmployeeCode(): void {
    // Only generate for new employees
    if (!this.isCreateMode) return;

    // Generate unique employee code
    const now = new Date();
    const datePart = this.formatDateForCode(now);
    
    // Generate a unique 4-digit random number
    const uniqueId = Math.floor(1000 + Math.random() * 9000);
    
    // Format: EMP20260205_1234
    const employeeCode = `EMP${datePart}${uniqueId}_FS`;
    
    this.employeeForm.patchValue({ 
      EmployeeCode: employeeCode 
    }, { emitEvent: false });
  }

  private formatDateForCode(date: Date): string {
    // Format: YYYYMMDD
    const year = date.getFullYear();
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    const day = date.getDate().toString().padStart(2, '0');
    return `${year}${month}${day}`;
  }

  private patchForm(employee: Employee): void {
    const formatDate = (dateString: string | null | undefined): string => {
      if (!dateString) return '';
      try {
        const date = new Date(dateString);
        return date.toISOString().split('T')[0];
      } catch {
        return '';
      }
    };

    this.employeeForm.patchValue({
      EmployeeId: employee.EmployeeId,
      EmployeeCode: employee.EmployeeCode, // Keep existing code for edit
      FirstName: employee.FirstName,
      LastName: employee.LastName,
      FatherName: employee.FatherName,
      MotherName: employee.MotherName,
      Gender: employee.Gender,
      DateOfBirth: formatDate(employee.DateOfBirth),
      Email: employee.Email,
      Phone: employee.Phone,
      DepartmentId: employee.DepartmentId ?? null,
      RoleId: employee.RoleId ?? null,
      DesignationId: employee.DesignationId ?? null,
      StartedOn: formatDate(employee.StartedOn),
      EndedOn: formatDate(employee.EndedOn),
      ResignedOn: formatDate(employee.ResignedOn),
      LastWorkingDay: formatDate(employee.LastWorkingDay),
      OfferRelesedOn: formatDate(employee.OfferRelesedOn),
      OfferAcceptedOn: formatDate(employee.OfferAcceptedOn),
      OfferPrice: employee.OfferPrice,
      CurrentPrice: employee.CurrentPrice,
      JoiningBonus: employee.JoiningBonus,
      UserId: employee.UserId,
      IsActive: employee.IsActive ?? true
    }, { emitEvent: false });
  }

  onSubmit(): void {
    if (this.employeeForm.invalid) {
      this.employeeForm.markAllAsTouched();
      return;
    }

    const formValue = this.employeeForm.value;
    
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
    this.resetForm();
    this.closeSidebar.emit();
  }

  private resetForm(): void {
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
  }
}