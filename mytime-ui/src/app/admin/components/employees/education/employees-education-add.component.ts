import { CommonModule } from '@angular/common';
import { 
  Component, 
  Input, 
  Output, 
  EventEmitter, 
  OnChanges, 
  SimpleChanges 
} from '@angular/core';
import { 
  ReactiveFormsModule, 
  FormBuilder, 
  FormGroup, 
  Validators 
} from '@angular/forms';
import { EmployeeEducation } from '../../../models/employee_education';

@Component({
  selector: 'app-employees-education-add',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './employees-education-add.component.html',
  styleUrls: ['./employees-education-add.component.css']
})
export class EmployeesEducationAddComponent implements OnChanges {
  @Input() education: EmployeeEducation | null = null;
  @Input() isVisible: boolean = false;
  @Output() save = new EventEmitter<EmployeeEducation>();
  @Output() close = new EventEmitter<void>();

  currentYear = new Date().getFullYear();
  years: number[] = [];
  
  educationForm: FormGroup;

  degrees = [
    { code: "SSC10", name: "Secondary School Certificate (10th)" },
    { code: "HSC12", name: "Higher Secondary Certificate (12th)" },
    { code: "DIPLOMA", name: "Diploma" },
    { code: "BTECH", name: "Bachelor of Technology" },
    { code: "BSC", name: "Bachelor of Science" },
    { code: "MSC", name: "Master of Science" },
    { code: "MTECH", name: "Master of Technology" },
    { code: "MBA", name: "Master of Business Administration" },
    { code: "BA", name: "Bachelor of Arts" },
    { code: "MA", name: "Master of Arts" },
    { code: "PHD", name: "Doctor of Philosophy" },
    { code: "BCOM", name: "Bachelor of Commerce" },
    { code: "MCOM", name: "Master of Commerce" }
  ];

  institutions = [
    { code: "OU", name: "Osmania University" },
    { code: "JNTU", name: "Jawaharlal Nehru Technological University" },
    { code: "KU", name: "Kakatiya University" },
    { code: "TU", name: "Telangana University" },
    { code: "MGU", name: "Mahatma Gandhi University" },
    { code: "PU", name: "Palamuru University" },
    { code: "SU", name: "Satavahana University" },
    { code: "RGUKT", name: "Rajiv Gandhi University of Knowledge Technologies" },
    { code: "TSBIE", name: "Telangana State Board of Intermediate Education" },
    { code: "TSBSE", name: "Telangana State Board of Secondary Education" },
    { code: "CBSE", name: "Central Board of Secondary Education" },
    { code: "ICSE", name: "Indian Certificate of Secondary Education" },
    { code: "NITW", name: "National Institute of Technology, Warangal" },
    { code: "IITH", name: "Indian Institute of Technology, Hyderabad" },
    { code: "IIITH", name: "International Institute of Information Technology, Hyderabad" }
  ];

  fieldOfStudies = [
    { code: "MPC", name: "Mathematics, Physics, Chemistry" },
    { code: "BIPC", name: "Biology, Physics, Chemistry" },
    { code: "CEC", name: "Commerce, Economics, Civics" },
    { code: "HEC", name: "History, Economics, Civics" },
    { code: "CS", name: "Computer Science" },
    { code: "IT", name: "Information Technology" },
    { code: "MECH", name: "Mechanical Engineering" },
    { code: "ELEC", name: "Electrical Engineering" },
    { code: "CIVIL", name: "Civil Engineering" },
    { code: "ECE", name: "Electronics and Communication Engineering" },
    { code: "CSE", name: "Computer Science Engineering" },
    { code: "BBA", name: "Business Administration" },
    { code: "MBA", name: "Master of Business Administration" },
    { code: "MCA", name: "Master of Computer Applications" },
    { code: "MSC_MATH", name: "Master of Science in Mathematics" },
    { code: "MSC_PHY", name: "Master of Science in Physics" },
    { code: "MSC_CHEM", name: "Master of Science in Chemistry" },
    { code: "MSC_CS", name: "Master of Science in Computer Science" },
    { code: "BA_ENG", name: "Bachelor of Arts in English" },
    { code: "BA_HIS", name: "Bachelor of Arts in History" },
    { code: "MA_ENG", name: "Master of Arts in English" },
    { code: "BCOM", name: "Bachelor of Commerce" },
    { code: "MCOM", name: "Master of Commerce" },
    { code: "MBBS", name: "Medicine" },
    { code: "PHARM", name: "Pharmacy" },
    { code: "LLB", name: "Law" },
    { code: "GENERAL", name: "General" }
  ];

  constructor(private fb: FormBuilder) {
    this.educationForm = this.fb.group({
      Degree: ['', Validators.required],
      FieldOfStudy: [''],
      Institution: [''],
      YearOfCompletion: [''],
      PercentageMarks: ['', [Validators.min(0), Validators.max(100)]],
      IsActive: [true]
    });
    
    this.generateYears();
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['education'] && this.education) {
      this.initializeForm();
    }
  }

  private generateYears(): void {
    const startYear = 1970;
    for (let year = this.currentYear; year >= startYear; year--) {
      this.years.push(year);
    }
  }

  private initializeForm(): void {
    if (this.education) {
      this.educationForm.patchValue({
        Degree: this.education.Degree || '',
        FieldOfStudy: this.education.FieldOfStudy || '',
        Institution: this.education.Institution || '',
        YearOfCompletion: this.education.YearOfCompletion || '',
        PercentageMarks: this.education.PercentageMarks || '',
        IsActive: this.education.IsActive !== undefined ? this.education.IsActive : true
      });
    } else {
      this.educationForm.reset({
        IsActive: true
      });
    }
  }

  onSubmit(): void {
    if (this.educationForm.valid) {
      const educationData: EmployeeEducation = {
        ...this.education,
        ...this.educationForm.value,
        EmployeeEducationId: this.education?.EmployeeEducationId || 0
      };
      
      this.save.emit(educationData);
    }
  }

  onClose(): void {
    this.close.emit();
  }
}