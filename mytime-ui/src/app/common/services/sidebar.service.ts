import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
@Injectable({
  providedIn: 'root'
})
export class SidebarService {
  private isCollapsed = new BehaviorSubject<boolean>(false);
  private isMobileOpen = new BehaviorSubject<boolean>(false);
  
  isCollapsed$ = this.isCollapsed.asObservable();
  isMobileOpen$ = this.isMobileOpen.asObservable();

  constructor() {
    this.init();
  }

  private init() {
    // Check initial screen size
    this.checkScreenSize();
    
    // Listen for window resize
    window.addEventListener('resize', () => {
      this.checkScreenSize();
    });

    // Listen for clicks on mobile to close sidebar when clicking outside
    document.addEventListener('click', (event) => {
      if (this.isMobileOpen.value && window.innerWidth < 992) {
        const target = event.target as HTMLElement;
        const sidebar = document.querySelector('.sidebar');
        const navbarToggler = document.querySelector('.navbar-toggler');
        
        if (sidebar && !sidebar.contains(target) && 
            navbarToggler && !navbarToggler.contains(target)) {
          this.closeMobileSidebar();
        }
      }
    });
  }

  private checkScreenSize() {
    const isMobile = window.innerWidth < 992;
    
    if (isMobile) {
      // On mobile, always expand sidebar and close mobile view
      this.isCollapsed.next(false);
      if (this.isMobileOpen.value) {
        // Don't close automatically, let user close
      }
    } else {
      // On desktop, close mobile sidebar if open
      if (this.isMobileOpen.value) {
        this.closeMobileSidebar();
      }
    }
  }

  toggleSidebar() {
    if (window.innerWidth < 992) {
      this.toggleMobileSidebar();
    } else {
      this.isCollapsed.next(!this.isCollapsed.value);
    }
  }

  toggleMobileSidebar() {
    const newState = !this.isMobileOpen.value;
    this.isMobileOpen.next(newState);
    
    if (newState) {
      document.body.classList.add('sidebar-open-mobile');
      document.body.style.overflow = 'hidden';
    } else {
      document.body.classList.remove('sidebar-open-mobile');
      document.body.style.overflow = '';
    }
  }

  closeMobileSidebar() {
    this.isMobileOpen.next(false);
    document.body.classList.remove('sidebar-open-mobile');
    document.body.style.overflow = '';
  }

  collapseSidebar() {
    if (window.innerWidth >= 992) {
      this.isCollapsed.next(true);
    }
  }

  expandSidebar() {
    if (window.innerWidth >= 992) {
      this.isCollapsed.next(false);
    }
  }
}