import { CommonModule } from '@angular/common';
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
import { TaskItem } from '../../../models/taskitem';

@Component({
  selector: 'app-create-taskitem',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule],
  templateUrl: './create-taskitem.component.html',
  styleUrl: './create-taskitem.component.css',
})
export class CreateTaskitemComponent implements OnInit, OnChanges {
  @Input() isVisible: boolean = false;
  @Input() taskitem: TaskItem | null = null;

  @Output() closeSidebar = new EventEmitter<void>();
  @Output() saveTaskItem = new EventEmitter<TaskItem>();

  taskitemForm: FormGroup;

  constructor(private fb: FormBuilder) {
    this.taskitemForm = this.fb.group({
      Name: ['', [Validators.required, Validators.maxLength(100)]],
      Code: ['', [Validators.required, Validators.maxLength(50), Validators.pattern(/^[a-zA-Z0-9_]+$/)]],

    });
  }

  ngOnChanges(changes: SimpleChanges): void {
    // Handle visibility changes
    if (changes['isVisible'] && changes['isVisible'].currentValue) {
      // Reset form when sidebar becomes visible for new role
      if (!this.taskitem?.TaskItemId) {
        this.resetForm();
      }

      // If document data is provided, patch it
      if (this.taskitem) {
        this.patchForm(this.taskitem);
      }
    }

    // Handle document input changes
    if (changes['taskitem']) {
      const task = changes['taskitem'].currentValue;
      if (task) {
        this.patchForm(task);
      } else if (!this.isVisible) {
        this.resetForm();
      }
    }
  }

  private patchForm(taskitem: TaskItem): void {
    this.taskitemForm.patchValue(
      {
        Name: taskitem.Name || '',
         Code: taskitem.Code || ''
      },
      { emitEvent: false },
    );

    // Mark form as pristine after patching existing data
    if (taskitem.TaskItemId) {
      this.taskitemForm.markAsPristine();
      this.taskitemForm.markAsUntouched();
    }
  }

  private resetForm(): void {
    this.taskitemForm.reset();
    this.taskitemForm.markAsPristine();
    this.taskitemForm.markAsUntouched();
  }
  ngOnInit(): void {
    // If document is provided on initialization, patch the form
    if (this.taskitem) {
      this.patchForm(this.taskitem);
    }
  }
  close(): void {
    this.resetForm();
    this.closeSidebar.emit();
  }
  onSubmit(): void {
    if (this.taskitemForm.valid) {
      const taskitemData: TaskItem = {
        ...this.taskitemForm.value,
        Id: this.taskitem?.TaskItemId || 0,
      };

      this.saveTaskItem.emit(taskitemData);
      this.resetForm();
    } else {
      // Mark all fields as touched to show validation errors
      this.taskitemForm.markAllAsTouched();
    }
  }
}
