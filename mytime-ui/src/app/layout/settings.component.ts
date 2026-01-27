import { Component } from '@angular/core';
import { AccountService } from '../common/services/account.service';

@Component({
  selector: 'app-settings',
  standalone: true,
  imports: [],
  templateUrl: './settings.component.html',
  styleUrl: './settings.component.css'
})
export class SettingsComponent {
  constructor(private accountService: AccountService) { }
  logout() {
    this.accountService.logout();
  }
}
