import { Component } from '@angular/core';
import { AccountService } from '../common/services/account.service';

@Component({
  selector: 'app-admin-sidebar',
  standalone: true,
  imports: [],
  templateUrl: './admin-sidebar.component.html',
  styleUrl: './admin-sidebar.component.css'
})
export class AdminSidebarComponent {
  constructor(private accountService: AccountService) {

  }
  logout(): void {
    this.accountService.logout();
  }
}
