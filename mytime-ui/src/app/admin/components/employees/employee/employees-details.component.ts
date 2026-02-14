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
import { EmployeesEducationListComponent } from '../education/employees-education-list.component';

// Models
import { Employee } from '../../../models/employee';
import { Department } from '../../../models/department';
import { Designation } from '../../../models/designation';
import { Role } from '../../../models/role';
import { EmployeeDTO } from '../../../models/employee.dto';
import { AuditFieldsService } from '../../../../common/services/auditfields.service';
import { EmployeesEmployementListComponent } from '../employment/employees-employement-list.component';

@Component({
  selector: 'app-employees-details',
  standalone: true,
  imports: [
    CommonModule,
    EmployeesCreateComponent,
    EmployeesEducationListComponent,
    EmployeesEmployementListComponent
  ],
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
  selectedEmployee: Employee | null = null;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private employeeService: EmployeeService,
    private departmentService: DepartmentService,
    private designationService: DesignationService,
    private roleService: RoleService,
    private loaderService: LoaderService,
    private toastr: ToastrService,
    private datePipe: DatePipe,
    private audit: AuditFieldsService
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

  // ========== UI ACTIONS ==========
  openEditForm(): void {
    this.selectedEmployee = this.employee;
    this.showEditForm = true;
  }

  closeEditForm(): void {
    this.showEditForm = false;
    this.selectedEmployee = null;
  }

  onEmployeeUpdated(updateEmployee: Employee): void {
    this.loaderService.show();

    const employeeDTO = this.convertEmployeeToDTO(updateEmployee);
    const _employee = this.audit.appendAuditFields(employeeDTO);

    this.employeeService.insertOrUpdateEmployee(_employee).subscribe({
      next: (response) => {
        if (response) {
          this.toastr.success("Employee processed successfully");
          this.showEditForm = false;
          this.employee = response.employee;
          this.selectedEmployee = this.employee;
          this.loaderService.hide();
        }
      },
      error: (error) => {
        console.error('Error updating employee:', error);
        this.toastr.error("Something went wrong, please check and resubmit");
        this.loaderService.hide();
      }
    });
  }

  private convertEmployeeToDTO(employee: Employee): EmployeeDTO {
    return {
      ...employee,
      DateOfBirth: this.parseDateString(employee.DateOfBirth),
      StartedOn: this.parseDateString(employee.StartedOn),
      EndedOn: this.parseDateString(employee.EndedOn),
      ResignedOn: this.parseDateString(employee.ResignedOn),
      LastWorkingDay: this.parseDateString(employee.LastWorkingDay),
      OfferRelesedOn: this.parseDateString(employee.OfferRelesedOn),
      OfferAcceptedOn: this.parseDateString(employee.OfferAcceptedOn),
      CreatedOn: this.parseDateString(employee.CreatedOn),
      ModifiedOn: this.parseDateString(employee.ModifiedOn)
    };
  }

  private parseDateString(dateString: string | null | undefined): Date | null {
    if (!dateString || dateString.trim() === '') {
      return null;
    }

    const date = new Date(dateString);
    return isNaN(date.getTime()) ? null : date;
  }

  goBack(): void {
    this.router.navigate(['/admin/employees']);
  }

  GetRoleName(roleId: any): string {
    if (!roleId || roleId <= 0) return "Not specified";

    const role = this.roles?.find(x => x.Id === roleId);
    return role ? role.Name : "Not specified";
  }

  GetDesignationName(designationId: any): string {
    if (!designationId || designationId <= 0) return "Not specified";

    const designation = this.designations?.find(x => x.DesignationId === designationId);
    return designation ? designation.Name : "Not specified";
  }

  GetDepartmentName(departmentId: any): string {
    if (!departmentId || departmentId <= 0) return "Not specified";

    const department = this.departments?.find(x => x.DepartmentId === departmentId);
    return department ? department.Name : "Not specified";
  }
}