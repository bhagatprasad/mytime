import { Component, Input } from '@angular/core';
import { AccountService } from '../common/services/account.service';

@Component({
  selector: 'app-user-sidebar',
  standalone: true,
  imports: [],
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
