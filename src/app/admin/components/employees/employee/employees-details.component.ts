import { Component, OnInit, AfterViewInit, OnDestroy, ChangeDetectorRef } from '@angular/core';
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
import { EmployeesEmergenceyContactListComponent } from '../contacts/employees-emergencey-contact-list.component';
import { ListDocumentsComponent } from '../documents/list.component';
import { EmployeesAddressesListComponent } from '../addresses/employees-addresses-list.component';

declare var bootstrap: any;

@Component({
  selector: 'app-employees-details',
  standalone: true,
  imports: [
    CommonModule,
    EmployeesCreateComponent,
    EmployeesEducationListComponent,
    EmployeesEmployementListComponent,
    EmployeesEmergenceyContactListComponent,
    ListDocumentsComponent,
    EmployeesAddressesListComponent
  ],
  providers: [DatePipe, CurrencyPipe],
  templateUrl: './employees-details.component.html',
  styleUrls: ['./employees-details.component.css']
})
export class EmployeesDetailsComponent implements OnInit, AfterViewInit, OnDestroy {
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
  isLoading: boolean = true; // Add this flag for template

  // Tab state management
  activeTab: string = 'personal';
  private tabElements: any;

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
    private audit: AuditFieldsService,
    private cdr: ChangeDetectorRef
  ) { }

  ngOnInit(): void {
    console.log('ngOnInit - Started');
    this.getEmployeeId();
    this.loadEmployeeDetails();

    this.route.queryParams.subscribe(params => {
      if (params['tab']) {
        this.activeTab = params['tab'];
        console.log('Tab from URL:', this.activeTab);
      }
    });
  }

  ngAfterViewInit(): void {
    console.log('ngAfterViewInit - View initialized');
  }

  ngOnDestroy(): void {
    console.log('ngOnDestroy - Cleaning up');
    if (this.tabElements) {
      this.tabElements.dispose();
    }
  }

  private getEmployeeId(): void {
    const id = this.route.snapshot.paramMap.get('employeeId');
    this.employeeId = id ? +id : 0;
    console.log('Employee ID:', this.employeeId);
  }

  private loadEmployeeDetails(): void {
    if (!this.employeeId) {
      console.log('No employee ID found');
      this.isLoading = false;
      this.loaderService.hide();
      return;
    }

    console.log('Loading employee details...');
    this.isLoading = true;
    this.loaderService.show();

    forkJoin({
      employee: this.employeeService.getEmployeeByIdAsync(this.employeeId),
      departments: this.departmentService.getDepartmentsListAsync(),
      designations: this.designationService.getDesignationsListAsync(),
      roles: this.roleService.getRoleListAsync()
    }).subscribe({
      next: (data) => {
        console.log('Data received:', data);

        // Set all the data
        this.employee = data.employee;
        this.departments = data.departments;
        this.designations = data.designations;
        this.roles = data.roles;

        console.log('Employee data set:', this.employee);

        // Force change detection
        this.cdr.detectChanges();

        // Use requestAnimationFrame to ensure DOM is updated
        requestAnimationFrame(() => {
          console.log('DOM updated, initializing tabs...');

          // Initialize tabs
          this.initializeTabs();

          // Switch to URL tab if needed
          if (this.activeTab !== 'personal') {
            setTimeout(() => {
              this.switchTab(this.activeTab);
            }, 50);
          }

          // Now hide loading states
          this.isLoading = false;
          this.loaderService.hide();

          console.log('Loading complete, UI should be visible now');
        });
      },
      error: (error) => {
        console.error('Error loading employee details:', error);
        this.toastr.error('Failed to load employee details');
        this.isLoading = false;
        this.loaderService.hide();
      }
    });
  }

  private initializeTabs(): void {
    console.log('Initializing tabs...');

    if (typeof bootstrap === 'undefined') {
      console.warn('Bootstrap JS is not loaded');
      return;
    }

    const tabElements = document.querySelectorAll('#employeeTabs button[data-bs-toggle="tab"]');
    console.log('Found tab elements:', tabElements.length);

    if (tabElements.length === 0) {
      console.warn('No tab elements found');
      return;
    }

    tabElements.forEach(tab => {
      tab.removeEventListener('shown.bs.tab', this.tabShownHandler);
      tab.addEventListener('shown.bs.tab', this.tabShownHandler.bind(this));
    });

    console.log('Tab event listeners added');
  }

  private tabShownHandler = (event: any): void => {
    if (event && event.target) {
      this.activeTab = event.target.id.replace('-tab', '');
      console.log('Tab changed to:', this.activeTab);

      this.router.navigate([], {
        relativeTo: this.route,
        queryParams: { tab: this.activeTab },
        queryParamsHandling: 'merge'
      });
    }
  }

  switchTab(tabId: string): void {
    console.log('Switching to tab:', tabId);

    if (!this.employee) {
      console.log('Employee not loaded yet');
      return;
    }

    if (typeof bootstrap === 'undefined') {
      console.warn('Bootstrap JS is not loaded');
      return;
    }

    const tabButton = document.getElementById(`${tabId}-tab`);
    console.log('Tab button:', tabButton);

    if (tabButton) {
      try {
        const bsTab = new bootstrap.Tab(tabButton);
        bsTab.show();
        console.log('Tab switched successfully');
      } catch (error) {
        console.error('Error switching tab:', error);
      }
    }
  }

  isTabActive(tabId: string): boolean {
    return this.activeTab === tabId;
  }

  getInitials(): string {
    if (!this.employee?.FirstName && !this.employee?.LastName) {
      return '??';
    }

    const first = this.employee.FirstName?.charAt(0) || '';
    const last = this.employee.LastName?.charAt(0) || '';
    return (first + last).toUpperCase();
  }

  getAvatarColor(): string {
    const colors = [
      '#667eea', '#764ba2', '#f43f5e', '#8b5cf6',
      '#ec4899', '#14b8a6', '#f97316', '#06b6d4'
    ];

    if (!this.employee?.FirstName) return colors[0];

    const index = this.employee.FirstName.length % colors.length;
    return colors[index];
  }

  openEditForm(): void {
    this.selectedEmployee = this.employee;
    this.showEditForm = true;
  }

  closeEditForm(): void {
    this.showEditForm = false;
    this.selectedEmployee = null;
  }

  onEmployeeUpdated(updateEmployee: Employee): void {
    console.log('Updating employee...');
    this.loaderService.show();

    const employeeDTO = this.convertEmployeeToDTO(updateEmployee);
    const _employee = this.audit.appendAuditFields(employeeDTO);

    this.employeeService.insertOrUpdateEmployee(_employee).subscribe({
      next: (response) => {
        console.log('Employee updated:', response);

        if (response) {
          this.toastr.success("Employee processed successfully");
          this.showEditForm = false;
          this.employee = response.employee;
          this.selectedEmployee = this.employee;

          this.cdr.detectChanges();

          requestAnimationFrame(() => {
            this.initializeTabs();
            this.loaderService.hide();
          });
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