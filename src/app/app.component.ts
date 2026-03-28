import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';
import { map, switchMap } from 'rxjs/operators';
import { combineLatest } from 'rxjs';

import { HeaderComponent } from './layout/header.component';
import { SidebarComponent } from './layout/sidebar.component';
import { FooterComponent } from './layout/footer.component';
import { TitleComponent } from './layout/title.component';
import { AccountService } from './common/services/account.service';
import { PanelLoaderComponent } from './common/components/loader.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    CommonModule,
    RouterOutlet,
    HeaderComponent,
    SidebarComponent,
    FooterComponent,
    TitleComponent,
    PanelLoaderComponent
  ],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  constructor(private accountService: AccountService) {}

  // Combine auth status with user data
  userContext$ = this.accountService.authStatus$.pipe(
    switchMap(authStatus => {
      if (authStatus.isLoading) {
        // Return loading state
        return [{
          isLoading: true,
          isAuthenticated: false,
          user: null,
          isAdmin: false,
          isAdministrator: false,
          isRegularAdmin: false,
          userRoleName: ''
        }];
      }

      // Combine with user data
      const user = authStatus.isAuthenticated ? this.accountService.getCurrentUser() : null;
      return [{
        isLoading: false,
        isAuthenticated: authStatus.isAuthenticated,
        user,
        isAdmin: authStatus.isAuthenticated && user ? this.accountService.isAdmin(user) : false,
        isAdministrator: authStatus.isAuthenticated && user ? this.accountService.isAdministrator(user) : false,
        isRegularAdmin: authStatus.isAuthenticated && user ? this.accountService.isRegularAdmin(user) : false,
        userRoleName: authStatus.isAuthenticated && user ? this.accountService.getUserRoleName(user) : ''
      }];
    })
  );
}