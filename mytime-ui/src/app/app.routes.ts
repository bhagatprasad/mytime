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
                path: 'dashboard',
                loadComponent: () => import('./dashbaord/admin-dashbaord.component').then(m => m.AdminDashbaordComponent)
            },
            {
                path: 'roles',
                loadComponent: () => import('./admin/components/role.component').then(m => m.RoleComponent)
            },
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