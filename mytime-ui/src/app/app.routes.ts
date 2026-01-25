import { Routes } from '@angular/router';
import { UserDashbaordComponent } from './dashbaord/user-dashbaord.component';
import { AdminDashbaordComponent } from './dashbaord/admin-dashbaord.component';

export const routes: Routes = [
    { path: '', redirectTo: 'adminbaord', pathMatch: 'full' },
    { path: 'userbaord', component: UserDashbaordComponent },
    { path: 'adminbaord', component: AdminDashbaordComponent },
    { path: '**', redirectTo: 'adminbaord' }
];
