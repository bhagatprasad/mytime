import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, OnChanges, Output, SimpleChanges } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { EmployeeDocument } from '../../../models/employee_document';
import { LoaderService } from '../../../../common/services/loader.service';
import { ToastrService } from 'ngx-toastr';
import { StorageService } from '../../../../common/services/storage.service';

@Component({
  selector: 'app-document-upload',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './upload.component.html',
  styleUrl: './upload.component.css'
})
export class UploadDocumentComponent implements OnChanges {
  @Input() employeeDocument: EmployeeDocument | null = null;
  @Input() isVisible: boolean = false;
  @Input() employeeId: number = 0;

  @Output() save = new EventEmitter<EmployeeDocument>();
  @Output() close = new EventEmitter<void>();

  documentForm: FormGroup;
  selectedFile: File | null = null;
  fileError: string = '';
  isUploading: boolean = false;

  documentTypes: string[] = [
    'Aadhar Card',
    'PAN Card',
    'Voter ID',
    'Passport',
    'Driving License',
    '10th Marksheet',
    '12th Marksheet',
    'Graduation Certificate',
    'Post Graduation Certificate',
    'Experience Letter',
    'Offer Letter',
    'Salary Slip',
    'Bank Statement',
    'Form 16',
    'Medical Certificate',
    'Insurance Policy',
    'Relieving Letter',
    'Other'
  ];

  private readonly allowedTypes = [
    'application/pdf',
    'image/jpeg',
    'image/jpg',
    'image/png',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.ms-excel',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
  ];

  private readonly maxFileSize = 10 * 1024 * 1024; // 10 MB

  constructor(
    private fb: FormBuilder,
    private storageService: StorageService,
    private loader: LoaderService,
    private notify: ToastrService
  ) {
    this.documentForm = this.fb.group({
      EmployeeDocumentId: [0],
      EmployeeId: [this.employeeId],
      DocumentType: ['', Validators.required],
      FileId: [''],
      FileName: [''],
      BucketId: [''],
      ContentLength: [0],
      ContentType: [''],
      FileInfo: [''],
      UploadTimestamp: [''],
      IsActive: [true]
    });
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['employeeDocument'] && this.employeeDocument) {
      this.initializeForm();
    }
    if (changes['employeeId'] && this.employeeId) {
      this.documentForm.patchValue({ EmployeeId: this.employeeId });
    }
    if (changes['isVisible'] && this.isVisible && !this.employeeDocument) {
      this.resetForm();
    }
  }

  private initializeForm(): void {
    if (this.employeeDocument) {
      this.documentForm.patchValue({
        EmployeeDocumentId: this.employeeDocument.EmployeeDocumentId || 0,
        EmployeeId: this.employeeDocument.EmployeeId || this.employeeId,
        DocumentType: this.employeeDocument.DocumentType || '',
        FileId: this.employeeDocument.FileId || '',
        FileName: this.employeeDocument.FileName || '',
        BucketId: this.employeeDocument.BucketId || '',
        ContentLength: this.employeeDocument.ContentLength || 0,
        ContentType: this.employeeDocument.ContentType || '',
        FileInfo: this.employeeDocument.FileInfo || '',
        UploadTimestamp: this.employeeDocument.UploadTimestamp || '',
        IsActive: this.employeeDocument.IsActive !== undefined ? this.employeeDocument.IsActive : true
      });
    }
  }

  private resetForm(): void {
    this.documentForm.reset({
      EmployeeDocumentId: 0,
      EmployeeId: this.employeeId,
      DocumentType: '',
      FileId: '',
      FileName: '',
      BucketId: '',
      ContentLength: 0,
      ContentType: '',
      FileInfo: '',
      UploadTimestamp: '',
      IsActive: true
    });
    this.selectedFile = null;
    this.fileError = '';
    this.isUploading = false;
  }

  onFileSelected(event: any): void {
    const file = event.target.files[0];
    if (file) this.validateAndSetFile(file);
  }

  onDragOver(event: DragEvent): void {
    event.preventDefault();
    event.stopPropagation();
  }

  onDrop(event: DragEvent): void {
    event.preventDefault();
    event.stopPropagation();
    const files = event.dataTransfer?.files;
    if (files && files.length > 0) {
      this.validateAndSetFile(files[0]);
    }
  }

  private validateAndSetFile(file: File): void {
    this.fileError = '';

    if (!this.allowedTypes.includes(file.type)) {
      this.fileError = 'File type not supported. Please upload PDF, JPG, PNG, DOC, DOCX, XLS, or XLSX files.';
      return;
    }

    if (file.size > this.maxFileSize) {
      this.fileError = 'File size exceeds 10MB limit. Please upload a smaller file.';
      return;
    }

    this.selectedFile = file;
    this.documentForm.patchValue({
      FileName: file.name,
      ContentLength: file.size,
      ContentType: file.type
    });
  }

  removeFile(): void {
    this.selectedFile = null;
    this.fileError = '';
    this.documentForm.patchValue({
      FileName: '',
      ContentLength: 0,
      ContentType: ''
    });
  }

  async onSubmit(): Promise<void> {
    if (this.documentForm.invalid) {
      Object.keys(this.documentForm.controls).forEach(key => {
        this.documentForm.get(key)?.markAsTouched();
      });
      return;
    }

    if (!this.selectedFile) {
      this.fileError = 'Please select a file to upload';
      return;
    }

    this.isUploading = true;
    this.loader.show();

    try {
      // Build prefix: employeeId_timestamp so stored file is identifiable
      const prefix = `${this.employeeId}_${Date.now()}`;

      const uploadResponse = await this.storageService.uploadFile(this.selectedFile, prefix);

      console.log('Upload response:', uploadResponse);

      const formValue = this.documentForm.value;

      const documentData: EmployeeDocument = {
        EmployeeDocumentId: formValue.EmployeeDocumentId || 0,
        EmployeeId: formValue.EmployeeId || this.employeeId,
        DocumentType: formValue.DocumentType,
        FileId: uploadResponse.fileId,           // unique B2 key — use this for download/delete
        FileName: uploadResponse.fileName,        // original file name shown to user
        BucketId: uploadResponse.storedFileName,  // actual stored name in B2
        ContentLength: uploadResponse.contentLength,
        ContentType: uploadResponse.contentType,
        FileInfo: JSON.stringify({
          downloadUrl: uploadResponse.downloadUrl,
          storedFileName: uploadResponse.storedFileName
        }),
        UploadTimestamp: new Date(uploadResponse.uploadTimestamp).toISOString(),
        CreatedOn: this.employeeDocument ? undefined : new Date().toISOString(),
        ModifiedOn: new Date().toISOString(),
        IsActive: formValue.IsActive
      };

      this.save.emit(documentData);
      this.notify.success('Document uploaded successfully');
      this.onClose();

    } catch (error: any) {
      console.error('Upload failed:', error);
      const detail = error?.error?.detail || 'Failed to upload document. Please try again.';
      this.notify.error(detail);
    } finally {
      this.isUploading = false;
      this.loader.hide();
    }
  }

  onClose(): void {
    this.resetForm();
    this.close.emit();
  }

  isFieldInvalid(fieldName: string): boolean {
    const field = this.documentForm.get(fieldName);
    return field ? (field.invalid && (field.dirty || field.touched)) : false;
  }

  getErrorMessage(fieldName: string): string {
    const field = this.documentForm.get(fieldName);
    if (field?.hasError('required')) {
      return fieldName === 'DocumentType' ? 'Please select a document type' : `${fieldName} is required`;
    }
    return '';
  }

  getFileIcon(): string {
    if (!this.selectedFile) return 'mdi-file-document';
    const type = this.selectedFile.type;
    if (type === 'application/pdf') return 'mdi-file-pdf-box';
    if (type.includes('image/')) return 'mdi-file-image';
    if (type.includes('word')) return 'mdi-file-word';
    if (type.includes('excel') || type.includes('spreadsheet')) return 'mdi-file-excel';
    return 'mdi-file-document';
  }

  getIconClass(): string {
    if (!this.selectedFile) return '';
    const type = this.selectedFile.type;
    if (type === 'application/pdf') return 'pdf';
    if (type.includes('image/')) return 'image';
    if (type.includes('word')) return 'word';
    if (type.includes('excel') || type.includes('spreadsheet')) return 'excel';
    return '';
  }

  formatFileSize(bytes: number): string {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }
}