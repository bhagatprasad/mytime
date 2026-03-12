import { Component, OnInit, HostListener } from '@angular/core';
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
export class HeaderComponent implements OnInit {
  isMobileMenuOpen = false;

  constructor(private sidebarService: SidebarService) {}

  ngOnInit(): void {
    // Subscribe to mobile menu state
    this.sidebarService.isMobileMenuOpen$.subscribe(isOpen => {
      this.isMobileMenuOpen = isOpen;
      this.updateMenuButtonState();
    });
  }

  toggleMobileMenu(): void {
    this.sidebarService.toggleMobileMenu();
  }

  private updateMenuButtonState(): void {
    const menuButton = document.querySelector('.navbar-toggler-right');
    if (menuButton) {
      if (this.isMobileMenuOpen) {
        menuButton.classList.add('menu-open');
      } else {
        menuButton.classList.remove('menu-open');
      }
    }
  }

  @HostListener('window:resize', ['$event'])
  onResize(): void {
    // Reset menu state on resize if needed
    if (window.innerWidth >= 992) {
      // On desktop, ensure menu is closed
      if (this.isMobileMenuOpen) {
        this.sidebarService.closeMobileMenu();
      }
    }
  }
}