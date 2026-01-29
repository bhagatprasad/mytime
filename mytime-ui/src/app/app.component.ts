import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';
import { map } from 'rxjs/operators';

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
    PanelLoaderComponent // Add this
  ],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {

   constructor(private accountService: AccountService) { }

  userContext$ = this.accountService.authenticationState$.pipe(
    map(isAuthenticated => {
      const user = isAuthenticated ? this.accountService.getCurrentUser() : null;
      return {
        isAuthenticated,
        user,
        isAdmin: isAuthenticated && user ? this.accountService.isAdmin(user) : false,
        isAdministrator: isAuthenticated && user ? this.accountService.isAdministrator(user) : false,
        isRegularAdmin: isAuthenticated && user ? this.accountService.isRegularAdmin(user) : false,
        userRoleName: isAuthenticated && user ? this.accountService.getUserRoleName(user) : ''
      };
    })
  );
}