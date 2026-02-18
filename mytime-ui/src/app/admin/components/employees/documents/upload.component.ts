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

  // Document types list
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

  // Allowed file types
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

  private readonly maxFileSize = 10 * 1024 * 1024;

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
      this.documentForm.patchValue({
        EmployeeId: this.employeeId
      });
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
    this.validateAndSetFile(file);
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

    // Validate file type
    if (!this.allowedTypes.includes(file.type)) {
      this.fileError = 'File type not supported. Please upload PDF, JPG, PNG, DOC, DOCX, XLS, or XLSX files.';
      return;
    }

    // Validate file size
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
      // Step 1: Upload to Backblaze B2
      console.log('Uploading to Backblaze B2...');
      
      const b2Response = await this.storageService.uploadFile(this.selectedFile, {
        fileName: `${this.employeeId}_${Date.now()}_${this.selectedFile.name}`,
        mime: this.selectedFile.type,
        fileInfo: {
          employeeId: this.employeeId.toString(),
          documentType: this.documentForm.get('DocumentType')?.value,
          uploadedBy: 'employee'
        }
      });

      console.log('B2 Upload Response:', b2Response);

      // Step 2: Prepare EmployeeDocument object with B2 response
      const formValue = this.documentForm.value;
      
      const documentData: EmployeeDocument = {
        EmployeeDocumentId: formValue.EmployeeDocumentId || 0,
        EmployeeId: formValue.EmployeeId || this.employeeId,
        DocumentType: formValue.DocumentType,
        FileId: b2Response.fileId,
        FileName: b2Response.fileName,
        BucketId: b2Response.bucketId,
        ContentLength: b2Response.contentLength,
        ContentType: b2Response.contentType,
        FileInfo: formValue.FileInfo || JSON.stringify(b2Response.fileInfo),
        UploadTimestamp: new Date(b2Response.uploadTimestamp).toISOString(),
        CreatedOn: this.employeeDocument ? undefined : new Date().toISOString(),
        ModifiedOn: new Date().toISOString(),
        IsActive: formValue.IsActive
      };

      console.log('Sending document data to parent:', documentData);
      
      // Step 3: Emit to parent component
      this.save.emit(documentData);
      
      this.notify.success('Document uploaded successfully');
      this.onClose();

    } catch (error) {
      console.error('Upload failed:', error);
      this.notify.error('Failed to upload document. Please try again.');
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
      if (fieldName === 'DocumentType') {
        return 'Please select a document type';
      }
      return `${fieldName} is required`;
    }
    return '';
  }
}