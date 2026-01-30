import { CommonModule, DatePipe } from '@angular/common';
import { Component, EventEmitter, Input, OnChanges, Output, SimpleChanges } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { Role } from '../models/role';

@Component({
  selector: 'app-create-role',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule],
  templateUrl: './create-role.component.html',
  styleUrl: './create-role.component.css',
  providers: [DatePipe]
})
export class CreateRoleComponent implements OnChanges {

  @Input() isVisible: boolean = false;

  @Output() closeSidebar = new EventEmitter<void>();

  @Output() saveRole = new EventEmitter<Role>();

  private _role: Role | null = null;

  roleForm: FormGroup;

  @Input()
  set role(value: Role | null) {
    console.log('Medicine input received:', value);
    this._role = value;
    if (value) {
      this.patchForm(value);
    }
  }
  get role(): Role | null {
    return this._role;
  }


  constructor(private fb: FormBuilder, private datePipe: DatePipe) {
    this.roleForm = this.fb.group({
      Name: ['', Validators.required],
      Code: ['', Validators.required]
    });
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['role'] && changes['role'].currentValue) {
      this.patchForm(changes['role'].currentValue);
    }
  }
  private patchForm(role: Role): void {
    const formattedData = {
      ...role
    };
    console.log('Patching form with:', formattedData);
    this.roleForm.patchValue(formattedData);
  }

  onSubmit(): void {
    if (this.roleForm.valid) {
      const roleData: Role = {
        ...this.roleForm.value,
        Id: this.role?.Id || 0,
      };
      this.saveRole.emit(roleData);
    }
  }
 close(): void {
    this.closeSidebar.emit();
  }
}
