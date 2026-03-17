import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, OnChanges, Output, SimpleChanges, OnInit, input } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { Role } from '../../../models/role';
import { Taskcode } from '../../../models/taskcode';
import { TaskItem } from '../../../models/taskitem';
import { forkJoin } from 'rxjs';
import { TaskcodeService } from '../../../services/taskcode.service';
import { TaskitemService } from '../../../services/taskitem.service';

@Component({
  selector: 'app-create-taskcode',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule],
  templateUrl: './create-taskcode.component.html',
 styleUrls: ['./create-taskcode-component.css']
})
export class CreateTaskcodeComponent implements OnChanges, OnInit {

  @Input() isVisible: boolean = false;
  @Input() taskcode: Taskcode | null = null;
  @Input() taskitems:TaskItem[]=[]
  
  @Output() closeSidebar = new EventEmitter<void>();
  @Output() saveTaskcode = new EventEmitter<Taskcode>();

  taskcodeForm: FormGroup;

  constructor(private fb: FormBuilder,private taskcodeservice:TaskcodeService,private taskitemservice:TaskitemService) {
    this.taskcodeForm = this.fb.group({
      Name: ['', [Validators.required, Validators.maxLength(100)]],
      Code: ['', [Validators.required, Validators.maxLength(50), Validators.pattern(/^[a-zA-Z0-9_]+$/)]],
      TaskItemId: ['', [Validators.required, Validators.maxLength(50), Validators.pattern(/^[0-9]+$/)]]
    });
  }

  ngOnInit(): void {
    // If role is provided on initialization, patch the form
    if (this.taskcode) {
      this.patchForm(this.taskcode);
    }
    this.loadIntialData()
  }

  ngOnChanges(changes: SimpleChanges): void {
    // Handle visibility changes
    if (changes['isVisible'] && changes['isVisible'].currentValue) {
      // Reset form when sidebar becomes visible for new role
      if (!this.taskcode?.TaskCodeId) {
        this.resetForm();
      }
      
      // If role data is provided, patch it
      if (this.taskcode) {
        this.patchForm(this.taskcode);
      }
    }
    
    // Handle role input changes
    if (changes['taskcode']) {
      const taskcode = changes['taskcode'].currentValue;
      if (taskcode) {
        this.patchForm(taskcode);
      } else if (!this.isVisible) {
        this.resetForm();
      }
    }
  }
loadIntialData(): void {

    forkJoin({
      taskitems: this.taskitemservice.GetTaskitemListAsync(),
      taskcode: this.taskcodeservice.getTaskcodeListAsync()
    }).subscribe({
      next: ({ taskitems, taskcode }) => {
        this.taskitems = taskitems;
        this.taskcode = taskcode;
      },
      error: (error) => {
        console.error('Error loading data:', error);
      }
    });
  }
  private patchForm(taskcode: Taskcode): void {
    this.taskcodeForm.patchValue({
      Name: taskcode.Name || '',
      Code: taskcode.Code || '',
      TaskItemId:taskcode.TaskItemId || '',
    }, { emitEvent: false });
    
    // Mark form as pristine after patching existing data
    if (taskcode.TaskCodeId) {
      this.taskcodeForm.markAsPristine();
      this.taskcodeForm.markAsUntouched();
    }
  }

  private resetForm(): void {
    this.taskcodeForm.reset();
    this.taskcodeForm.markAsPristine();
    this.taskcodeForm.markAsUntouched();
  }

  close(): void {
    this.resetForm();
    this.closeSidebar.emit();
  }

  onSubmit(): void {
    if (this.taskcodeForm.valid) {
      const taskcodedata: Taskcode = {
        ...this.taskcodeForm.value,
        TaskCodeId: this.taskcode?.TaskCodeId || 0
      };
      
      this.saveTaskcode.emit(taskcodedata);
      this.resetForm();
    } else {
      // Mark all fields as touched to show validation errors
      this.taskcodeForm.markAllAsTouched();
    }
  }
}