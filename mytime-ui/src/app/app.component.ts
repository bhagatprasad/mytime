import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';
import { map } from 'rxjs/operators';

import { HeaderComponent } from './layout/header.component';
import { SidebarComponent } from './layout/sidebar.component';
import { FooterComponent } from './layout/footer.component';
import { TitleComponent } from './layout/title.component';
import { AccountService } from './common/services/account.service';
import { LoaderService } from './common/services/loader.service'; // Add this
import { ApplicationUser } from './common/models/application-user';
import { PanelLoaderComponent } from './common/components/loader.component';

interface UserContext {
  isAuthenticated: boolean | null;
  user: ApplicationUser | null;
  isAdmin: boolean;
  isAdministrator: boolean;
  isRegularAdmin: boolean;
  userRoleName: string;
}

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
export class AppComponent implements OnInit {
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

  constructor(
    private accountService: AccountService,
    private loaderService: LoaderService
  ) { }

  ngOnInit() {
    // Show loader in main panel while loading app
    this.loaderService.show();
    
    // Hide after 1.5 seconds
    setTimeout(() => {
      this.loaderService.hide();
    }, 1500);
  }
}