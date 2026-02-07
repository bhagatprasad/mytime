import { Component, OnInit } from '@angular/core';
import { CommonModule, CurrencyPipe, DatePipe } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { forkJoin } from 'rxjs';

// Services
import { EmployeeService } from '../../../services/employee.service';
import { DepartmentService } from '../../../services/department.service';
import { DesignationService } from '../../../services/designation.service';
import { RoleService } from '../../../services/role.service';
import { LoaderService } from '../../../../common/services/loader.service';
import { ToastrService } from 'ngx-toastr';

// Components
import { EmployeesCreateComponent } from './employees-create.component';

// Models
import { Employee } from '../../../models/employee';
import { Department } from '../../../models/department';
import { Designation } from '../../../models/designation';
import { Role } from '../../../models/role';

@Component({
  selector: 'app-employees-details',
  standalone: true,
  imports: [CommonModule, EmployeesCreateComponent],
  providers: [DatePipe, CurrencyPipe],
  templateUrl: './employees-details.component.html',
  styleUrls: ['./employees-details.component.css']
})
export class EmployeesDetailsComponent implements OnInit {
  // Employee Data
  employee: Employee | null = null;
  employeeId: number = 0;

  // Reference Data
  departments: Department[] = [];
  designations: Designation[] = [];
  roles: Role[] = [];

  // UI State
  showEditForm = false;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private employeeService: EmployeeService,
    private departmentService: DepartmentService,
    private designationService: DesignationService,
    private roleService: RoleService,
    private loaderService: LoaderService,
    private toastr: ToastrService,
    private datePipe: DatePipe
  ) { }

  ngOnInit(): void {
    this.getEmployeeId();
    this.loadEmployeeDetails();
  }

  // ========== DATA LOADING ==========
  private getEmployeeId(): void {
    const id = this.route.snapshot.paramMap.get('employeeId');
    this.employeeId = id ? +id : 0;
  }

  private loadEmployeeDetails(): void {
    if (!this.employeeId) return;
    this.loaderService.show();

    forkJoin({
      employee: this.employeeService.getEmployeeByIdAsync(this.employeeId),
      departments: this.departmentService.getDepartmentsListAsync(),
      designations: this.designationService.getDesignationsListAsync(),
      roles: this.roleService.getRoleListAsync()
    }).subscribe({
      next: (data) => {
        this.employee = data.employee;
        this.departments = data.departments;
        this.designations = data.designations;
        this.roles = data.roles;
        this.loaderService.hide();
      },
      error: (error) => {
        console.error('Error loading employee details:', error);
        this.toastr.error('Failed to load employee details');
        this.loaderService.hide();
      }
    });
  }

  // ========== HELPER METHODS ==========
  getInitials(): string {
    if (!this.employee?.FirstName && !this.employee?.LastName) {
      return '??';
    }

    const first = this.employee.FirstName?.charAt(0) || '';
    const last = this.employee.LastName?.charAt(0) || '';
    return (first + last).toUpperCase();
  }

  formatDate(dateString: string | null | undefined): string {
    if (!dateString) return 'Not specified';

    try {
      const date = new Date(dateString);
      return this.datePipe.transform(date, 'dd/MM/yyyy') || dateString;
    } catch {
      return dateString;
    }
  }

  formatCurrency(amount: number | null | undefined): string {
    if (amount === null || amount === undefined) return 'Not specified';
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      minimumFractionDigits: 0,
      maximumFractionDigits: 2
    }).format(amount);
  }

  // ========== UI ACTIONS ==========
  openEditForm(): void {
    this.showEditForm = true;
  }

  closeEditForm(): void {
    this.showEditForm = false;
  }

  onEmployeeUpdated(updatedEmployee: Employee): void {
    if (updatedEmployee) {
      this.employee = { ...this.employee, ...updatedEmployee };
      this.toastr.success('Employee updated successfully');
      this.closeEditForm();
    }
  }

  goBack(): void {
    this.router.navigate(['/admin/employees']);
  }
}