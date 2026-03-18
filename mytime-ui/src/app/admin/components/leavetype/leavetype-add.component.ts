import {
  Component,
  EventEmitter,
  Input,
  OnChanges,
  OnInit,
  Output,
  SimpleChanges,
} from '@angular/core';
import {
  FormBuilder,
  FormGroup,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import { LeaveType } from '../../models/leave-type.model';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-leavetype-add',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule],
  templateUrl: './leavetype-add.component.html',
  styleUrl: './leavetype-add.component.css',
})
export class LeavetypeAddComponent implements OnInit, OnChanges {
  @Input() isVisible: boolean = false;
  @Input() leavetype: LeaveType | null = null;
  @Output() closeSidebar = new EventEmitter<void>();
  @Output() saveLeaveType = new EventEmitter<LeaveType>();

  leavetypeForm: FormGroup;

  constructor(private fb: FormBuilder) {
    this.leavetypeForm = this.fb.group({
      Name: ['', [Validators.required, Validators.maxLength(100)]],
      MaxDaysPerYear: [
        '',
        [Validators.required, Validators.min(1), Validators.max(365)],
      ],
      Description: [
        '',
        [
          Validators.required,
          Validators.minLength(11),
          Validators.maxLength(250),
        ],
      ],
    });
  }

  ngOnInit(): void {
    // If leavetype is provided on initialization, patch the form
    if (this.leavetype) {
      this.patchForm(this.leavetype);
    }
  }
  ngOnChanges(changes: SimpleChanges): void {
    // Handle visibility changes
    if (changes['isVisible'] && changes['isVisible'].currentValue) {
      // Reset form when sidebar becomes visible for new leavetype
      if (!this.leavetype?.Id) {
        this.resetForm();
      }

      // If leavetype data is provided, patch it
      if (this.leavetype) {
        this.patchForm(this.leavetype);
      }
    }

    // Handle role input changes
    if (changes['leavetype']) {
      const leavetype = changes['leavetype'].currentValue;
      if (leavetype) {
        this.patchForm(leavetype);
      } else if (!this.isVisible) {
        this.resetForm();
      }
    }
  }

  private patchForm(leavetype: LeaveType): void {
    this.leavetypeForm.patchValue(
      {
        Name: leavetype.Name || '',
        MaxDaysPerYear: leavetype.MaxDaysPerYear || '',
        Description: leavetype.Description || '',
      },
      { emitEvent: false },
    );

    // Mark form as pristine after patching existing data
    if (leavetype.Id) {
      this.leavetypeForm.markAsPristine();
      this.leavetypeForm.markAsUntouched();
    }
  }

  private resetForm(): void {
    this.leavetypeForm.reset();
    this.leavetypeForm.markAsPristine();
    this.leavetypeForm.markAsUntouched();
  }

  close(): void {
    this.resetForm();
    this.closeSidebar.emit();
  }

  onSubmit(): void {
    if (this.leavetypeForm.valid) {
      const leavetypeData: LeaveType = {
        ...this.leavetypeForm.value,
        Id: this.leavetype?.Id || 0,
      };

      this.saveLeaveType.emit(leavetypeData);
      this.resetForm();
    } else {
      // Mark all fields as touched to show validation errors
      this.leavetypeForm.markAllAsTouched();
    }
  }
}
