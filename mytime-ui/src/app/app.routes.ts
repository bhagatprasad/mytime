import { Routes } from '@angular/router';
import { UserGuard } from './common/gurds/user.guard';
import { AdminGuard } from './common/gurds/admin.guard';

export const routes: Routes = [
    {
        path: 'login',
        loadComponent: () => import('./common/components/login.component').then(m => m.LoginComponent)
    },
    {
        path: 'user',
        canActivate: [UserGuard],
        children: [
            {
                path: 'dashboard',
                loadComponent: () => import('./dashbaord/user-dashbaord.component').then(m => m.UserDashbaordComponent)
            },
            {
                path: '',
                redirectTo: 'dashboard',
                pathMatch: 'full'
            }
        ]
    },
    {
        path: 'admin',
        canActivate: [AdminGuard],
        children: [
            {
                path: 'cities',
                loadComponent: () => import('./admin/components/city-list.component').then(m => m.CityListComponent)
            },
            {
                path: 'countries',
                loadComponent: () => import('./admin/components/country-list.component').then(m => m.CountryListComponent)
            },
            {
                path: 'dashboard',
                loadComponent: () => import('./dashbaord/admin-dashbaord.component').then(m => m.AdminDashbaordComponent)
            },
            {
                path: 'departments',
                loadComponent: () => import('./admin/components/department-list.component').then(m => m.DepartmentListComponent)
            },
            {
                path: 'designations',
                loadComponent: () => import('./admin/components/designation-list.component').then(m => m.DesignationListComponent)
            },
            {
                path: 'documenttypes',
                loadComponent: () => import('./admin/components/documenttype-list.component').then(m => m.DocumenttypeListComponent)
            },
            {
                path: 'holydaycallenders',
                loadComponent: () => import('./admin/components/holydaycallender-list.component').then(m => m.HolydaycallenderListComponent)
            },
            {
                path: 'roles',
                loadComponent: () => import('./admin/components/role.component').then(m => m.RoleComponent)
            },
            {
                path: 'states',
                loadComponent: () => import('./admin/components/state-list.component').then(m => m.StateListComponent)
            },
            {
                path: 'users',
                loadComponent: () => import('./admin/components/user-list.component').then(m => m.UserListComponent)
            },
            // ========== EMPLOYEES ROUTES ==========
            {
                path: 'employees',
                children: [
                    {
                        path: '',
                        loadComponent: () => import('./admin/components/employees/employee/employees-list.component').then(m => m.EmployeesListComponent)
                    },
                    {
                        path: ':employeeId',
                        loadComponent: () => import('./admin/components/employees/employee/employees-details.component').then(m => m.EmployeesDetailsComponent)
                    }
                ]
            },
            // ======================================
            {
                path: '',
                redirectTo: 'dashboard',
                pathMatch: 'full'
            }
        ]
    },
    {
        path: '',
        redirectTo: 'login',
        pathMatch: 'full'
    },
    {
        path: '**',
        redirectTo: 'login'
    }
];