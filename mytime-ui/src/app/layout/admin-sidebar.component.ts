import { Component, Input, Inject, PLATFORM_ID } from '@angular/core';
import { AccountService } from '../common/services/account.service';
import { RouterModule, Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { SidebarService } from '../common/services/sidebar.service';
import { BaseSidebarComponent } from './base-sidebar.component';

@Component({
  selector: 'app-admin-sidebar',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './admin-sidebar.component.html',
  styleUrls: ['./admin-sidebar.component.css']
})
export class AdminSidebarComponent extends BaseSidebarComponent {
  @Input() isCollapsed = false;

  constructor(
    private accountService: AccountService,
    router: Router,
    sidebarService: SidebarService,
    @Inject(PLATFORM_ID) platformId: Object
  ) {
    super(router, sidebarService, platformId);
  }

  logout(): void {
    this.accountService.logout();
    this.closeSidebarOnMobile();
  }
}