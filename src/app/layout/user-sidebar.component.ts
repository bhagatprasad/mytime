import { Component, Input } from '@angular/core';
import { AccountService } from '../common/services/account.service';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-user-sidebar',
  standalone: true,
  imports: [RouterModule],
  templateUrl: './user-sidebar.component.html',
  styleUrl: './user-sidebar.component.css'
})
export class UserSidebarComponent {
 @Input() isCollapsed = false;
  constructor(private accountService: AccountService) {
 
   }
   logout(): void {
     this.accountService.logout();
   }
}
