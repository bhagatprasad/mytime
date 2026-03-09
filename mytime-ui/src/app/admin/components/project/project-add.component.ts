import {
  Component,
  EventEmitter,
  Input,
  OnChanges,
  OnInit,
  Output,
  SimpleChanges,
} from '@angular/core';
import { Project } from '../../models/project';
import {
  FormBuilder,
  FormGroup,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-project-add',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule],
  templateUrl: './project-add.component.html',
  styleUrl: './project-add.component.css',
})
export class ProjectAddComponent implements OnInit, OnChanges {
  @Input() isVisible: boolean = false;
  @Input() project: Project | null = null;

  @Output() closeSidebar = new EventEmitter<void>();
  @Output() saveProject = new EventEmitter<Project>();

  projectForm: FormGroup;

  constructor(private fb: FormBuilder) {
    this.projectForm = this.fb.group({
      Name: ['', [Validators.required, Validators.maxLength(100)]],
    });
  }

  ngOnInit(): void {
    // If project is provided on initialization, patch the form
    if (this.project) {
      this.patchForm(this.project);
    }
  }

  ngOnChanges(changes: SimpleChanges): void {
    // Handle visibility changes
    if (changes['isVisible'] && changes['isVisible'].currentValue) {
      // Reset form when sidebar becomes visible for new project
      if (!this.project?.ProjectId) {
        this.resetForm();
      }

      // If project data is provided, patch it
      if (this.project) {
        this.patchForm(this.project);
      }
    }

    // Handle project input changes
    if (changes['project']) {
      const project = changes['project'].currentValue;
      if (project) {
        this.patchForm(project);
      } else if (!this.isVisible) {
        this.resetForm();
      }
    }
  }

  private resetForm(): void {
    this.projectForm.reset();
    this.projectForm.markAsPristine();
    this.projectForm.markAsUntouched();
  }
  close(): void {
    this.resetForm();
    this.closeSidebar.emit();
  }
  private patchForm(project: Project): void {
    this.projectForm.patchValue(
      {
        Name: project.Name || '',
      },
      { emitEvent: false },
    );

    // Mark form as pristine after patching existing data
    if (project.ProjectId) {
      this.projectForm.markAsPristine();
      this.projectForm.markAsUntouched();
    }
  }

  onSubmit(): void {
    if (this.projectForm.valid) {
      const projectData: Project = {
        ...this.projectForm.value,
        ProjectId: this.project?.ProjectId || 0,
      };

      this.saveProject.emit(projectData);
      this.resetForm();
    } else {
      // Mark all fields as touched to show validation errors
      this.projectForm.markAllAsTouched();
    }
  }
}
