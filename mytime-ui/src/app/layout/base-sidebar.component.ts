import { Component, OnInit, OnDestroy, Inject, PLATFORM_ID } from '@angular/core';
import { NavigationEnd, Router } from '@angular/router';
import { filter, Subscription } from 'rxjs';
import { isPlatformBrowser } from '@angular/common';
import { SidebarService } from '../common/services/sidebar.service';

@Component({
  template: '' // Abstract base component
})
export abstract class BaseSidebarComponent implements OnInit, OnDestroy {
  private routerSubscription!: Subscription;

  constructor(
    protected router: Router,
    protected sidebarService: SidebarService,
    @Inject(PLATFORM_ID) protected platformId: Object
  ) {}

  ngOnInit(): void {
    // Auto-close sidebar on mobile when navigation completes
    this.routerSubscription = this.router.events
      .pipe(filter(event => event instanceof NavigationEnd))
      .subscribe(() => {
        this.closeSidebarOnMobile();
      });
  }

  ngOnDestroy(): void {
    if (this.routerSubscription) {
      this.routerSubscription.unsubscribe();
    }
  }

  // Call this method on any link click
  onLinkClick(): void {
    this.closeSidebarOnMobile();
  }

  // Handle dropdown toggles without closing sidebar
  onDropdownToggle(event: Event, dropdownId: string): void {
    event.preventDefault();
    const dropdownElement = document.getElementById(dropdownId);
    if (dropdownElement) {
      dropdownElement.classList.toggle('show');
      
      // Update aria-expanded
      const toggleLink = event.currentTarget as HTMLElement;
      const isExpanded = toggleLink.getAttribute('aria-expanded') === 'true';
      toggleLink.setAttribute('aria-expanded', (!isExpanded).toString());
    }
    // Don't close sidebar - this is just dropdown toggle
    event.stopPropagation();
  }

  closeSidebarOnMobile(): void {
    if (isPlatformBrowser(this.platformId) && window.innerWidth < 992) {
      // Small delay to ensure navigation starts before closing
      setTimeout(() => {
        this.sidebarService.closeMobileMenu();
      }, 50);
    }
  }
}