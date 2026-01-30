import { Component } from '@angular/core';
import { NotificationsComponent } from './notifications.component';
import { SettingsComponent } from './settings.component';
import { SidebarService } from '../common/services/sidebar.service';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [NotificationsComponent, SettingsComponent],
  templateUrl: './header.component.html',
  styleUrl: './header.component.css'
})
export class HeaderComponent {
 constructor(private sidebarService: SidebarService) {}

  toggleMobileMenu(): void {
    this.sidebarService.toggleMobileMenu();
  }
}
