import { Component, Input } from '@angular/core';
import { AccountService } from '../common/services/account.service';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-admin-sidebar',
  standalone: true,
  imports: [RouterModule],
  templateUrl: './admin-sidebar.component.html',
  styleUrl: './admin-sidebar.component.css'
})
export class AdminSidebarComponent {
   @Input() isCollapsed = false;
  constructor(private accountService: AccountService) {

  }
  logout(): void {
    this.accountService.logout();
  }
}
