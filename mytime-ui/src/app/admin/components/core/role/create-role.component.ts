import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, OnChanges, Output, SimpleChanges, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { Role } from '../../../models/role';

@Component({
  selector: 'app-create-role',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule],
  templateUrl: './create-role.component.html',
  styleUrls: ['./create-role.component.css']
})
export class CreateRoleComponent implements OnChanges, OnInit {

  @Input() isVisible: boolean = false;
  @Input() role: Role | null = null;
  
  @Output() closeSidebar = new EventEmitter<void>();
  @Output() saveRole = new EventEmitter<Role>();

  roleForm: FormGroup;

  constructor(private fb: FormBuilder) {
    this.roleForm = this.fb.group({
      Name: ['', [Validators.required, Validators.maxLength(100)]],
      Code: ['', [Validators.required, Validators.maxLength(50), Validators.pattern(/^[a-zA-Z0-9_]+$/)]]
    });
  }

  ngOnInit(): void {
    // If role is provided on initialization, patch the form
    if (this.role) {
      this.patchForm(this.role);
    }
  }

  ngOnChanges(changes: SimpleChanges): void {
    // Handle visibility changes
    if (changes['isVisible'] && changes['isVisible'].currentValue) {
      // Reset form when sidebar becomes visible for new role
      if (!this.role?.Id) {
        this.resetForm();
      }
      
      // If role data is provided, patch it
      if (this.role) {
        this.patchForm(this.role);
      }
    }
    
    // Handle role input changes
    if (changes['role']) {
      const role = changes['role'].currentValue;
      if (role) {
        this.patchForm(role);
      } else if (!this.isVisible) {
        this.resetForm();
      }
    }
  }

  private patchForm(role: Role): void {
    this.roleForm.patchValue({
      Name: role.Name || '',
      Code: role.Code || ''
    }, { emitEvent: false });
    
    // Mark form as pristine after patching existing data
    if (role.Id) {
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
      const roleData: Role = {
        ...this.roleForm.value,
        Id: this.role?.Id || 0
      };
      
      this.saveRole.emit(roleData);
      this.resetForm();
    } else {
      // Mark all fields as touched to show validation errors
      this.roleForm.markAllAsTouched();
    }
  }
}