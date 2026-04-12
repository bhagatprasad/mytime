import { Component, OnInit, HostListener } from '@angular/core';
import { AccountService } from '../common/services/account.service';
import { AdminSidebarComponent } from './admin-sidebar.component';
import { UserSidebarComponent } from './user-sidebar.component';
import { map } from 'rxjs/operators';
import { CommonModule } from '@angular/common';
import { SidebarService } from '../common/services/sidebar.service';


@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [AdminSidebarComponent, UserSidebarComponent, CommonModule],
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.css']
})
export class SidebarComponent implements OnInit {
  
  isMobileMenuOpen = false;
  isMobileScreen = false;
  
  userContext$ = this.accountService.authenticationState$.pipe(
    map(isAuthenticated => {
      const user = isAuthenticated ? this.accountService.getCurrentUser() : null;

      return {
        isAuthenticated,
        user,
        roleId: user?.roleId ?? null,
        isAdminUser: user?.roleId === 1000 || user?.roleId === 1001
      };
    })
  );

  constructor(
    private accountService: AccountService,
    private sidebarService: SidebarService
  ) {}

  ngOnInit(): void {
    // Check initial screen size
    this.checkScreenSize();
    
    // Subscribe to mobile menu state
    this.sidebarService.isMobileMenuOpen$.subscribe(isOpen => {
      this.isMobileMenuOpen = isOpen;
      this.updateSidebarVisibility();
    });
  }

  @HostListener('window:resize', ['$event'])
  onResize(): void {
    this.checkScreenSize();
  }

  private checkScreenSize(): void {
    this.isMobileScreen = window.innerWidth < 992; // Bootstrap's lg breakpoint
    
    // On mobile screens, ensure sidebar is closed by default
    if (this.isMobileScreen) {
      this.isMobileMenuOpen = false;
    } else {
      // On desktop, always show sidebar
      this.isMobileMenuOpen = true;
    }
    
    this.updateSidebarVisibility();
  }

  private updateSidebarVisibility(): void {
    const sidebarElement = document.getElementById('sidebar');
    if (sidebarElement) {
      if (this.isMobileScreen) {
        // On mobile: toggle visibility based on isMobileMenuOpen
        if (this.isMobileMenuOpen) {
          sidebarElement.classList.add('mobile-visible');
          sidebarElement.classList.remove('mobile-hidden');
        } else {
          sidebarElement.classList.add('mobile-hidden');
          sidebarElement.classList.remove('mobile-visible');
        }
      } else {
        // On desktop: always visible
        sidebarElement.classList.add('desktop-visible');
        sidebarElement.classList.remove('mobile-hidden', 'mobile-visible');
      }
    }
  }

  // Close sidebar when clicking on overlay (for mobile)
  closeSidebarOnMobile(): void {
    if (this.isMobileScreen) {
      this.sidebarService.closeMobileMenu();
    }
  }
}