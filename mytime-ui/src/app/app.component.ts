import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';
import { map } from 'rxjs/operators';

import { HeaderComponent } from './layout/header.component';
import { SidebarComponent } from './layout/sidebar.component';
import { FooterComponent } from './layout/footer.component';
import { TitleComponent } from './layout/title.component';
import { AccountService } from './common/services/account.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    CommonModule,
    RouterOutlet,
    HeaderComponent,
    SidebarComponent,
    FooterComponent,
    TitleComponent
  ],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {

  isAuthenticated$ = this.accountService.authenticationState$;

  userContext$ = this.accountService.authenticationState$.pipe(
    map(isAuthenticated => ({
      isAuthenticated, // 👈 THIS WAS MISSING
      isAdmin: isAuthenticated && this.accountService.isAdmin(),
      isAdministrator: isAuthenticated && this.accountService.isAdministrator(),
      isRegularAdmin: isAuthenticated && this.accountService.isRegularAdmin(),
      userRoleName: isAuthenticated ? this.accountService.getUserRoleName() : ''
    }))
  );
  constructor(private accountService: AccountService) { }
}
