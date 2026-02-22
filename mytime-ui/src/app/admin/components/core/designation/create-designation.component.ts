import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, Output, SimpleChanges } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { Designation } from '../../../models/designation';

@Component({
  selector: 'app-create-designation',
  standalone: true,
  imports: [CommonModule,ReactiveFormsModule],
  templateUrl: './create-designation.component.html',
  styleUrl: './create-designation.component.css'
})
export class CreateDesignationComponent {

  @Input() isVisible: boolean = false;
  @Input() designation: Designation | null = null;

  @Output() closeSidebar = new EventEmitter<void>();
  @Output() saveDesignation = new EventEmitter<Designation>();

  roleForm: FormGroup;

  constructor(private fb: FormBuilder) {
    this.roleForm = this.fb.group({
      Name: ['', [Validators.required, Validators.maxLength(100)]],
      Code: ['', [Validators.required, Validators.maxLength(50), Validators.pattern(/^[a-zA-Z0-9_]+$/)]]
    });
  }

  ngOnInit(): void {
    // If role is provided on initialization, patch the form
    if (this.designation) {
      this.patchForm(this.designation);
    }
  }

  ngOnChanges(changes: SimpleChanges): void {
    // Handle visibility changes
    if (changes['isVisible'] && changes['isVisible'].currentValue) {
      // Reset form when sidebar becomes visible for new role
      if (!this.designation?.DesignationId) {
        this.resetForm();
      }

      // If role data is provided, patch it
      if (this.designation) {
        this.patchForm(this.designation);
      }
    }

    // Handle role input changes
    if (changes['designation']) {
      const des = changes['designation'].currentValue;
      if (des) {
        this.patchForm(des);
      } else if (!this.isVisible) {
        this.resetForm();
      }
    }
  }

  private patchForm(des: Designation): void {
    this.roleForm.patchValue({
      Name: des.Name || '',
      Code: des.Code || ''
    }, { emitEvent: false });

    // Mark form as pristine after patching existing data
    if (des.DesignationId) {
      this.roleForm.markAsPristine();
      this.roleForm.markAsUntouched();
    }
  }

  private resetForm(): void {
    this.roleForm.reset();
    this.roleForm.markAsPristine();
    this.roleForm.markAsUntouched();
  }

  close(): void {
    this.resetForm();
    this.closeSidebar.emit();
  }

  onSubmit(): void {
    if (this.roleForm.valid) {
      const designationData: Designation = {
        ...this.roleForm.value,
        DesignationId: this.designation?.DesignationId || 0
      };

      this.saveDesignation.emit(designationData);
      this.resetForm();
    } else {
      // Mark all fields as touched to show validation errors
      this.roleForm.markAllAsTouched();
    }
  }

}
