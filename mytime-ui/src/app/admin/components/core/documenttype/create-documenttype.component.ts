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
import { DocumentType } from '../../../models/document_type';

@Component({
  selector: 'app-create-documenttype',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule],
  templateUrl: './create-documenttype.component.html',
  styleUrl: './create-documenttype.component.css',
})
export class CreateDocumenttypeComponent implements OnInit, OnChanges {
  @Input() isVisible: boolean = false;
  @Input() documenttype: DocumentType | null = null;

  @Output() closeSidebar = new EventEmitter<void>();
  @Output() saveDocumentType = new EventEmitter<DocumentType>();

  documentForm: FormGroup;

  constructor(private fb: FormBuilder) {
    this.documentForm = this.fb.group({
      Name: ['', [Validators.required, Validators.maxLength(100)]],
      Code: [
        '',
        [
          Validators.required,
          Validators.maxLength(50),
          Validators.pattern(/^[a-zA-Z0-9_]+$/),
        ],
      ],
    });
  }

  ngOnChanges(changes: SimpleChanges): void {
    // Handle visibility changes
    if (changes['isVisible'] && changes['isVisible'].currentValue) {
      // Reset form when sidebar becomes visible for new role
      if (!this.documenttype?.Id) {
        this.resetForm();
      }

      // If document data is provided, patch it
      if (this.documenttype) {
        this.patchForm(this.documenttype);
      }
    }

    // Handle document input changes
    if (changes['documenttype']) {
      const document = changes['documenttype'].currentValue;
      if (document) {
        this.patchForm(document);
      } else if (!this.isVisible) {
        this.resetForm();
      }
    }
  }

  private patchForm(document: DocumentType): void {
    this.documentForm.patchValue(
      {
        Name: document.Name || '',
      },
      { emitEvent: false },
    );

    // Mark form as pristine after patching existing data
    if (document.Id) {
      this.documentForm.markAsPristine();
      this.documentForm.markAsUntouched();
    }
  }

  private resetForm(): void {
    this.documentForm.reset();
    this.documentForm.markAsPristine();
    this.documentForm.markAsUntouched();
  }
  ngOnInit(): void {
    // If document is provided on initialization, patch the form
    if (this.documenttype) {
      this.patchForm(this.documenttype);
    }
  }
  close(): void {
    this.resetForm();
    this.closeSidebar.emit();
  }
  onSubmit(): void {
    if (this.documentForm.valid) {
      const documentData: DocumentType = {
        ...this.documentForm.value,
        Id: this.documenttype?.Id || 0,
      };

      this.saveDocumentType.emit(documentData);
      this.resetForm();
    } else {
      // Mark all fields as touched to show validation errors
      this.documentForm.markAllAsTouched();
    }
  }
}
