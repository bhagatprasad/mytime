import { Component, OnInit } from '@angular/core';
import { AccountService } from '../common/services/account.service';
import { AdminSidebarComponent } from './admin-sidebar.component';
import { UserSidebarComponent } from './user-sidebar.component';
import { map } from 'rxjs/operators';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [AdminSidebarComponent, UserSidebarComponent,CommonModule],
  templateUrl: './sidebar.component.html',
  styleUrl: './sidebar.component.css'
})
export class SidebarComponent implements OnInit {

  userContext$ = this.accountService.authenticationState$.pipe(
    map(isAuthenticated => {
      const user = isAuthenticated ? this.accountService.getCurrentUser() : null;

      return {
        isAuthenticated,
        user,
        roleId: user?.roleId ?? null,
        isAdminUser: user?.roleId === 1000 || user?.roleId === 1001
      };
    })
  );

  constructor(private accountService: AccountService) {}

  ngOnInit(): void {}
}
