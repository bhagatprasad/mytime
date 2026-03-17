import { Routes } from '@angular/router';
import { UserGuard } from './common/gurds/user.guard';
import { AdminGuard } from './common/gurds/admin.guard';

export const routes: Routes = [
  // Public — no guard
  {
    path: 'login',
    loadComponent: () =>
      import('./common/components/login.component').then(
        (m) => m.LoginComponent,
      ),
  },

  // User routes — protected by UserGuard
  // UserGuard: must be authenticated AND not an admin
  {
    path: 'user',
    canActivate: [UserGuard],
    children: [
      {
        path: 'dashboard',
        loadComponent: () =>
          import('./dashbaord/user-dashbaord.component').then(
            (m) => m.UserDashbaordComponent,
          ),
      },
      {
        path: 'payslips',
        loadComponent: () =>
          import('./user/components/payslips/payslips.component').then(
            (m) => m.PayslipsComponent,
          ),
      },
      {
        path: 'ytdreports',
        loadComponent: () =>
          import('./user/components/ytdreports/ytdreports.component').then(
            (m) => m.YtdreportsComponent,
          ),
      },
      {
        path: '',
        redirectTo: 'dashboard',
        pathMatch: 'full',
      },
      {
        path: 'holidaycalendar',
        loadComponent: () =>
          import('./user/components/holidaycalendar/holidaycalendar.component').then(
            (m) => m.HolidaycalendarComponent,
          ),
      },
      {
        path: 'leaveapply',
        loadComponent: () =>
          import('./user/components/leaveapply/leaveapply.component').then(
            (m) => m.LeaveapplyComponent,
          ),
      },
      {
        path: 'payslips',
        loadComponent: () =>
          import('./user/components/payslips/payslips.component').then(
            (m) => m.PayslipsComponent,
          ),
      },
    ],
  },

  // Admin routes — protected by AdminGuard
  // AdminGuard: must be authenticated AND have roleId 1000 or 1001
  {
    path: 'admin',
    canActivate: [AdminGuard],
    children: [
      {
        path: 'dashboard',
        loadComponent: () =>
          import('./dashbaord/admin-dashbaord.component').then(
            (m) => m.AdminDashbaordComponent,
          ),
      },
      {
        path: 'cities',
        loadComponent: () =>
          import('./admin/components/core/city/city-list.component').then(
            (m) => m.CityListComponent,
          ),
      },
      {
        path: 'countries',
        loadComponent: () =>
          import('./admin/components/core/country/country-list.component').then(
            (m) => m.CountryListComponent,
          ),
      },
      {
        path: 'departments',
        loadComponent: () =>
          import('./admin/components/core/department/department-list.component').then(
            (m) => m.DepartmentListComponent,
          ),
      },
      {
        path: 'designations',
        loadComponent: () =>
          import('./admin/components/core/designation/designation-list.component').then(
            (m) => m.DesignationListComponent,
          ),
      },
      {
        path: 'documenttypes',
        loadComponent: () =>
          import('./admin/components/core/documenttype/documenttype-list.component').then(
            (m) => m.DocumenttypeListComponent,
          ),
      },
      {
        path: 'taskitem',
        loadComponent: () =>
          import('./admin/components/core/taskitem/taskitem-list.component').then(
            (m) => m.TaskItemListComponent,
          ),
      },
      {
        path: 'holydaycallenders',
        loadComponent: () =>
          import('./admin/components/core/holydaycallender/holydaycallender-list.component').then(
            (m) => m.HolydaycallenderListComponent,
          ),
      },
      {
        path: 'leavetype',
        loadComponent: () =>
          import('./admin/components/leavetype/leavetype-list.component').then(
            (m) => m.LeavetypeListComponent,
          ),
      },
      {
        path: 'roles',
        loadComponent: () =>
          import('./admin/components/core/role/role.component').then(
            (m) => m.RoleComponent,
          ),
      },
      {
        path: 'states',
        loadComponent: () =>
          import('./admin/components/core/state/state-list.component').then(
            (m) => m.StateListComponent,
          ),
      },
      {
        path: 'users',
        loadComponent: () =>
          import('./admin/components/user/user-list.component').then(
            (m) => m.UserListComponent,
          ),
      },
      {
        path: 'employees',
        children: [
          {
            path: '',
            loadComponent: () =>
              import('./admin/components/employees/employee/employees-list.component').then(
                (m) => m.EmployeesListComponent,
              ),
          },
          {
            path: 'documents',
            loadComponent: () =>
              import('./admin/components/employees/documents/employee-documents-list.component').then(
                (m) => m.EmployeeDocumentsListComponent,
              ),
          },
          {
            path: ':employeeId',
            loadComponent: () =>
              import('./admin/components/employees/employee/employees-details.component').then(
                (m) => m.EmployeesDetailsComponent,
              ),
          },
        ],
      },
      {
        path: 'salary',
        loadComponent: () =>
          import('./admin/components/salary/salary-list.component').then(
            (m) => m.SalaryListComponent,
          ),
      },
      {
        path: 'project',
        loadComponent: () =>
          import('./admin/components/project/project-list.component').then(
            (m) => m.ProjectListComponent,
          ),
      },
      {
        path: 'salary-structure',
        loadComponent: () =>
          import('./admin/components/salary/salary-structure-list.component').then(
            (m) => m.SalaryStructureListComponent,
          ),
      },
      {
        path: 'monthly-salary',
        loadComponent: () =>
          import('./admin/components/salary/monthly-salary-list.component').then(
            (m) => m.MonthlySalaryListComponent,
          ),
      },
      {
        path: 'taskcode',
        loadComponent: () =>
          import('./admin/components/time/taskcode/taskcode.component').then(
            (m) => m.TaskcodeComponent,
          ),
      },
      {
        path: 'leaves',
        loadComponent: () =>
          import('./admin/components/leaves/apply-leave.component').then(
            (m) => m.ApplyLeaveComponent,
          ),
      },
      {
        path: 'taskitem',
        loadComponent: () =>
          import('./admin/components/core/taskitem/taskitem-list.component').then(
            (m) => m.TaskItemListComponent,
          ),
      },
      {
        path: '',
        redirectTo: 'dashboard',
        pathMatch: 'full',
      },
    ],
  },

  // Fallbacks
  { path: '', redirectTo: 'login', pathMatch: 'full' },
  { path: '**', redirectTo: 'login' },
];
