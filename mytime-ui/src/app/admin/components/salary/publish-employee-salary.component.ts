import { Component, EventEmitter, HostListener, Input, Output, SimpleChanges } from '@angular/core';
import { EmployeeSalary } from '../../models/employee_salary';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { Employee } from '../../models/employee';
import { MultipleEmployeesMonthlySalaries } from '../../models/multiple_employees_monthly_salaries';

@Component({
  selector: 'app-publish-employee-salary',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './publish-employee-salary.component.html',
  styleUrl: './publish-employee-salary.component.css'
})
export class PublishEmployeeSalaryComponent {

  @Input() isVisible: boolean = false;
  @Input() employees: Employee[] = [];

  @Output() closeSidebar = new EventEmitter<void>();
  @Output() saveSalary = new EventEmitter<MultipleEmployeesMonthlySalaries>();

  salaryForm: FormGroup;

  employeeDropdownOpen = false;
  monthDropdownOpen = false;

  selectedEmployees: number[] = [];
  years: number[] = [];
  selectedMonths: number[] = [];
  selectedYear: number | null = null;

  months = [
    { id: 1, name: 'January' },
    { id: 2, name: 'February' },
    { id: 3, name: 'March' },
    { id: 4, name: 'April' },
    { id: 5, name: 'May' },
    { id: 6, name: 'June' },
    { id: 7, name: 'July' },
    { id: 8, name: 'August' },
    { id: 9, name: 'September' },
    { id: 10, name: 'October' },
    { id: 11, name: 'November' },
    { id: 12, name: 'December' }
  ];

  constructor(private fb: FormBuilder) {

    const currentYear = new Date().getFullYear();
    const currentMonth = new Date().getMonth() + 1;

    this.salaryForm = this.fb.group({
      EmployeeId: [[], Validators.required],
      SalaryYear: [currentYear, Validators.required],
      SalaryMonth: [[currentMonth], Validators.required]
    });

    for (let i = currentYear; i >= 2010; i--) {
      this.years.push(i);
    }

    this.selectedMonths = [currentMonth];
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['isVisible'] && this.isVisible) {
      this.resetForm();
    }
  }

  @HostListener('document:click', ['$event'])
  closeDropdowns(event: Event) {

    const target = event.target as HTMLElement;

    if (!target.closest('.form-group')) {
      this.employeeDropdownOpen = false;
      this.monthDropdownOpen = false;
    }

  }

  toggleEmployeeDropdown() {
    this.employeeDropdownOpen = !this.employeeDropdownOpen;
  }

  toggleMonthDropdown() {
    this.monthDropdownOpen = !this.monthDropdownOpen;
  }

  toggleEmployee(empId: any) {

    const index = this.selectedEmployees.indexOf(empId);

    if (index > -1) {
      this.selectedEmployees.splice(index, 1);
    } else {
      this.selectedEmployees.push(empId);
    }

    this.salaryForm.patchValue({
      EmployeeId: this.selectedEmployees
    });
  }

  toggleMonth(monthId: any) {

    const index = this.selectedMonths.indexOf(monthId);

    if (index > -1) {
      this.selectedMonths.splice(index, 1);
    } else {
      this.selectedMonths.push(monthId);
    }

    this.salaryForm.patchValue({
      SalaryMonth: this.selectedMonths
    });
  }

  getEmployeeLabel() {

    if (this.selectedEmployees.length === 0) {
      return 'Select Employee';
    }

    return `${this.selectedEmployees.length} Employees Selected`;
  }

  getMonthLabel() {

    if (this.selectedMonths.length === 0) {
      return 'Select Month';
    }

    if (this.selectedMonths.length === 1) {
      const month = this.months.find(x => x.id === this.selectedMonths[0]);
      return month?.name;
    }

    return `${this.selectedMonths.length} Months Selected`;
  }

  close() {
    this.resetForm();
    this.closeSidebar.emit();
  }

  resetForm() {

    const currentYear = new Date().getFullYear();
    const currentMonth = new Date().getMonth() + 1;

    this.selectedEmployees = [];
    this.selectedMonths = [currentMonth];

    this.salaryForm.reset({
      EmployeeId: [],
      SalaryYear: currentYear,
      SalaryMonth: [currentMonth]
    });

    this.employeeDropdownOpen = false;
    this.monthDropdownOpen = false;
  }

  submit() {

    if (this.salaryForm.valid) {

      const data: MultipleEmployeesMonthlySalaries = {
        EmployeeId: this.selectedEmployees.join(','),
        SalaryMonth: this.selectedMonths.join(','),
        SalaryYear: this.selectedYear?.toString() || null
      };

      this.saveSalary.emit(data);
      this.resetForm();
    }
  }
}