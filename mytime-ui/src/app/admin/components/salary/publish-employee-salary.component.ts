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

  months = [
    { id: 1,  name: 'January'   },
    { id: 2,  name: 'February'  },
    { id: 3,  name: 'March'     },
    { id: 4,  name: 'April'     },
    { id: 5,  name: 'May'       },
    { id: 6,  name: 'June'      },
    { id: 7,  name: 'July'      },
    { id: 8,  name: 'August'    },
    { id: 9,  name: 'September' },
    { id: 10, name: 'October'   },
    { id: 11, name: 'November'  },
    { id: 12, name: 'December'  }
  ];

  constructor(private fb: FormBuilder) {

    const currentYear  = new Date().getFullYear();
    const currentMonth = new Date().getMonth() + 1;

    this.salaryForm = this.fb.group({
      EmployeeId: [[], Validators.required],
      SalaryYear:  [currentYear,     Validators.required],
      SalaryMonth: [[currentMonth],  Validators.required]
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
      this.monthDropdownOpen    = false;
    }
  }

  toggleEmployeeDropdown() {
    this.employeeDropdownOpen = !this.employeeDropdownOpen;
    this.monthDropdownOpen    = false;
  }

  toggleMonthDropdown() {
    this.monthDropdownOpen    = !this.monthDropdownOpen;
    this.employeeDropdownOpen = false;
  }

  toggleEmployee(empId: number) {
    const index = this.selectedEmployees.indexOf(empId);
    if (index > -1) {
      this.selectedEmployees.splice(index, 1);
    } else {
      this.selectedEmployees.push(empId);
    }
    this.salaryForm.patchValue({ EmployeeId: this.selectedEmployees });
    this.salaryForm.get('EmployeeId')?.markAsTouched();
  }

  toggleMonth(monthId: number) {
    const index = this.selectedMonths.indexOf(monthId);
    if (index > -1) {
      this.selectedMonths.splice(index, 1);
    } else {
      this.selectedMonths.push(monthId);
    }
    this.salaryForm.patchValue({ SalaryMonth: this.selectedMonths });
    this.salaryForm.get('SalaryMonth')?.markAsTouched();
  }

  getEmployeeLabel(): string {
    if (this.selectedEmployees.length === 0) return 'Select Employee';
    if (this.selectedEmployees.length === 1) {
      const emp = this.employees.find(e => e.EmployeeId === this.selectedEmployees[0]);
      return emp ? `${emp.FirstName} ${emp.LastName}` : '1 Employee Selected';
    }
    return `${this.selectedEmployees.length} Employees Selected`;
  }

  getMonthLabel(): string {
    if (this.selectedMonths.length === 0) return 'Select Month';
    if (this.selectedMonths.length === 1) {
      return this.months.find(m => m.id === this.selectedMonths[0])?.name || 'Select Month';
    }
    return `${this.selectedMonths.length} Months Selected`;
  }

  isEmployeeSelected(empId: number): boolean {
    return this.selectedEmployees.includes(empId);
  }

  isMonthSelected(monthId: number): boolean {
    return this.selectedMonths.includes(monthId);
  }

  close() {
    this.resetForm();
    this.closeSidebar.emit();
  }

  resetForm() {
    const currentYear  = new Date().getFullYear();
    const currentMonth = new Date().getMonth() + 1;

    this.selectedEmployees    = [];
    this.selectedMonths       = [currentMonth];
    this.employeeDropdownOpen = false;
    this.monthDropdownOpen    = false;

    this.salaryForm.reset({
      EmployeeId:  [],
      SalaryYear:  currentYear,
      SalaryMonth: [currentMonth]
    });
  }

  submit() {
    if (this.salaryForm.valid) {

      // Map selected month IDs → month names  e.g. [1, 3] → "January,March"
      const selectedMonthNames = this.selectedMonths
        .map(id => this.months.find(m => m.id === id)?.name || '')
        .filter(name => name !== '')
        .join(',');

      const data: MultipleEmployeesMonthlySalaries = {
        EmployeeIds:  this.selectedEmployees.join(','),
        SalaryMonths: selectedMonthNames,
        SalaryYear:   this.salaryForm.value.SalaryYear?.toString() || null,
        CreatedBy:    1
      };

      this.saveSalary.emit(data);
      this.resetForm();
    }
  }
}