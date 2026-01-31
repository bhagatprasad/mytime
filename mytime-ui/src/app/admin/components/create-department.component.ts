import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, OnChanges, OnInit, Output, SimpleChanges } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { Department } from '../models/department';

@Component({
  selector: 'app-create-department',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './create-department.component.html',
  styleUrl: './create-department.component.css'
})
export class CreateDepartmentComponent implements OnChanges, OnInit {

  @Input() isVisible: boolean = false;
  @Input() department: Department | null = null;
  @Output() closeSidebar = new EventEmitter<void>();
  @Output() saveDepartment = new EventEmitter<Department>();

  departmentForm: FormGroup;
  
  constructor(private fb: FormBuilder) {
    this.departmentForm = this.fb.group({
      Name: ['', [Validators.required, Validators.maxLength(100)]],
      Code: ['', [Validators.required, Validators.maxLength(10)]],
      Description: ['', [Validators.required]]
    });
  }

  ngOnInit(): void {
    if (this.department) {
      this.patchForm(this.department);
    }
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['isVisible'] && changes['isVisible'].currentValue) {
      if (this.department) {
        this.patchForm(this.department);
      } else {
        this.resetForm();
      }
    }

    if (changes['department']) {
      const department = changes['department'].currentValue;
      if (department) {
        this.patchForm(department);
      } else {
        this.resetForm();
      }
    }
  }

  private patchForm(department: Department): void {
    this.departmentForm.patchValue({
      Name: department.Name || '',
      Code: department.Code || '',
      Description: department.Description || ''
    });
  }

  private resetForm(): void {
    this.departmentForm.reset();
    this.departmentForm.markAsPristine();
    this.departmentForm.markAsUntouched();
  }

  close(): void {
    this.closeSidebar.emit();
  }

  onSubmit(): void {
    if (this.departmentForm.valid) {
      const formValue = this.departmentForm.value;
      const departmentData: Department = {
        ...formValue,
        DepartmentId: this.department?.DepartmentId || 0
      };
      this.saveDepartment.emit(departmentData);
      this.close();
    } else {
      this.departmentForm.markAllAsTouched();
    }
  }
}