import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, OnChanges, Output, SimpleChanges, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { MonthlySalary } from '../../models/monlty_salary';

@Component({
  selector: 'app-monthly-salary-add',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule],
  templateUrl: './monthly-salary-add.component.html',
  styleUrls: ['./monthly-salary-add.component.css']
})
export class MonthlySalaryAddComponent implements OnChanges, OnInit {

  @Input() isVisible: boolean = false;
  @Input() monthlySalary: MonthlySalary | null = null;
  
  @Output() closeSidebar = new EventEmitter<void>();
  @Output() saveMonthlySalary = new EventEmitter<MonthlySalary>();

  monthlySalaryForm!: FormGroup;
  yearList: number[] = [];
  currentMonth: string = '';
  currentYear: number = 0;

  constructor(private fb: FormBuilder) {
    this.setCurrentDateTime();
    this.generateYearList();
    this.initializeForm();
  }

  private setCurrentDateTime(): void {
    const today = new Date();
    this.currentYear = today.getFullYear();
    const monthIndex = today.getMonth();
    const months = [
      'January', 'February', 'March', 'April', 'May', 'June',
      'July', 'August', 'September', 'October', 'November', 'December'
    ];
    this.currentMonth = months[monthIndex];
  }

  private generateYearList(): void {
    const startYear = 2000;
    const endYear = this.currentYear + 5;
    for (let year = startYear; year <= endYear; year++) {
      this.yearList.push(year);
    }
  }

  private initializeForm(): void {
    this.monthlySalaryForm = this.fb.group({
      Title: ['', [Validators.required, Validators.maxLength(200)]],
      SalaryMonth: [this.currentMonth, [Validators.required]],
      SalaryYear: [this.currentYear, [Validators.required]],
      Location: ['Hyderabad'],
      StdDays: [{ value: null, disabled: true }],
      WrkDays: [0, [Validators.required, Validators.min(0), Validators.max(31)]],
      LopDays: [0, [Validators.required, Validators.min(0), Validators.max(31)]]
    });

    setTimeout(() => {
      this.calculateDays();
    });
  }

  ngOnInit(): void {
    if (this.monthlySalary) {
      this.patchForm(this.monthlySalary);
    }
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['isVisible'] && changes['isVisible'].currentValue === true) {
      if (this.monthlySalary) {
        this.patchForm(this.monthlySalary);
      } else {
        this.resetToDefault();
      }
    }
    
    if (changes['monthlySalary']) {
      const monthlySalary = changes['monthlySalary'].currentValue;
      if (this.isVisible && monthlySalary) {
        this.patchForm(monthlySalary);
      }
    }
  }

  calculateDays(): void {
    const month = this.monthlySalaryForm.get('SalaryMonth')?.value;
    const year = this.monthlySalaryForm.get('SalaryYear')?.value;
    
    if (month && year) {
      const daysInMonth = this.getDaysInMonth(month, parseInt(year));
      
      this.monthlySalaryForm.patchValue({
        StdDays: daysInMonth
      });

      this.updateDaysValidators(daysInMonth);
    }
  }

  private updateDaysValidators(maxDays: number): void {
    const wrkDaysControl = this.monthlySalaryForm.get('WrkDays');
    const lopDaysControl = this.monthlySalaryForm.get('LopDays');
    
    if (wrkDaysControl && lopDaysControl) {
      wrkDaysControl.setValidators([Validators.required, Validators.min(0), Validators.max(maxDays)]);
      lopDaysControl.setValidators([Validators.required, Validators.min(0), Validators.max(maxDays)]);
      
      wrkDaysControl.updateValueAndValidity();
      lopDaysControl.updateValueAndValidity();
    }
  }

  private getDaysInMonth(month: string, year: number): number {
    const monthMap: { [key: string]: number } = {
      'January': 0, 'February': 1, 'March': 2, 'April': 3,
      'May': 4, 'June': 5, 'July': 6, 'August': 7,
      'September': 8, 'October': 9, 'November': 10, 'December': 11
    };
    
    const monthIndex = monthMap[month];
    if (monthIndex === undefined) return 0;
    
    return new Date(year, monthIndex + 1, 0).getDate();
  }

  getMonthDetails(): string {
    const month = this.monthlySalaryForm.get('SalaryMonth')?.value;
    const year = this.monthlySalaryForm.get('SalaryYear')?.value;
    
    if (month === 'February' && year) {
      const isLeapYear = this.isLeapYear(parseInt(year));
      return isLeapYear ? 'Leap Year' : 'Non-Leap Year';
    }
    return '';
  }

  getPayableDays(): number {
    const stdDays = this.monthlySalaryForm.get('StdDays')?.value || 0;
    const lopDays = this.monthlySalaryForm.get('LopDays')?.value || 0;
    return stdDays - lopDays;
  }

  private isLeapYear(year: number): boolean {
    return (year % 4 === 0 && year % 100 !== 0) || year % 400 === 0;
  }

  private patchForm(monthlySalary: MonthlySalary): void {
    this.monthlySalaryForm.get('StdDays')?.enable({ emitEvent: false });
    
    this.monthlySalaryForm.patchValue({
      Title: monthlySalary.Title || '',
      SalaryMonth: monthlySalary.SalaryMonth || this.currentMonth,
      SalaryYear: monthlySalary.SalaryYear || this.currentYear,
      Location: monthlySalary.Location || 'Hyderabad',
      StdDays: monthlySalary.StdDays,
      WrkDays: monthlySalary.WrkDays || 0,
      LopDays: monthlySalary.LopDays || 0
    });
    
    this.monthlySalaryForm.get('StdDays')?.disable({ emitEvent: false });
    
    if (monthlySalary.StdDays) {
      this.updateDaysValidators(monthlySalary.StdDays);
    }
  }

  private resetToDefault(): void {
    this.monthlySalaryForm.get('StdDays')?.enable({ emitEvent: false });
    
    this.monthlySalaryForm.reset({
      Title: '',
      SalaryMonth: this.currentMonth,
      SalaryYear: this.currentYear,
      Location: 'Hyderabad',
      WrkDays: 0,
      LopDays: 0
    });
    
    this.monthlySalaryForm.get('StdDays')?.disable({ emitEvent: false });
    
    this.monthlySalaryForm.markAsPristine();
    this.monthlySalaryForm.markAsUntouched();
    
    this.calculateDays();
  }

  close(): void {
    this.resetToDefault();
    this.closeSidebar.emit();
  }

  onSubmit(): void {
    if (this.monthlySalaryForm.valid) {
      this.monthlySalaryForm.get('StdDays')?.enable({ emitEvent: false });
      
      const formValue = this.monthlySalaryForm.value;
      
      const monthlySalaryData: MonthlySalary = {
        MonthlySalaryId: this.monthlySalary?.MonthlySalaryId || null,
        Title: formValue.Title,
        SalaryMonth: formValue.SalaryMonth,
        SalaryYear: formValue.SalaryYear.toString(),
        Location: formValue.Location,
        StdDays: formValue.StdDays,
        WrkDays: formValue.WrkDays,
        LopDays: formValue.LopDays,
        CreatedOn: null,
        CreatedBy: null,
        ModifiedOn: null,
        ModifiedBy: null,
        IsActive: null
      };
      
      this.monthlySalaryForm.get('StdDays')?.disable({ emitEvent: false });
      
      this.saveMonthlySalary.emit(monthlySalaryData);
      this.close();
    } else {
      this.monthlySalaryForm.markAllAsTouched();
    }
  }

  isFieldInvalid(fieldName: string): boolean {
    const field = this.monthlySalaryForm.get(fieldName);
    return field ? (field.invalid && (field.dirty || field.touched)) : false;
  }

  get formValid(): boolean {
    return this.monthlySalaryForm.valid;
  }

  validateTotalDays(): boolean {
    const stdDays = this.monthlySalaryForm.get('StdDays')?.value || 0;
    const wrkDays = this.monthlySalaryForm.get('WrkDays')?.value || 0;
    const lopDays = this.monthlySalaryForm.get('LopDays')?.value || 0;
    
    return (wrkDays + lopDays) <= stdDays;
  }
}