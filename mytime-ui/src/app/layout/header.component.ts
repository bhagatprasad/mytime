import { Component } from '@angular/core';
import { NotificationsComponent } from './notifications.component';
import { SettingsComponent } from './settings.component';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [NotificationsComponent,SettingsComponent],
  templateUrl: './header.component.html',
  styleUrl: './header.component.css'
})
export class HeaderComponent {

}
