import { Component, OnInit, OnDestroy, HostListener } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Store } from '@ngrx/store';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';

import { SidebarService } from '../common/services/sidebar.service';
import { AdminSidebarComponent } from './admin-sidebar.component';
import { UserSidebarComponent } from './user-sidebar.component';
import { selectUserContext } from '../common/store/auth.selectors';
import { ProfileImageComponent } from './profile-image.component';

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [
    CommonModule,
    AdminSidebarComponent,
    UserSidebarComponent,
    ProfileImageComponent, // ← added
  ],
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.css'],
})
export class SidebarComponent implements OnInit, OnDestroy {

  isMobileMenuOpen = false;
  isMobileScreen   = false;

  private readonly destroy$ = new Subject<void>();

  readonly userContext$ = this.store.select(selectUserContext);

  constructor(
    private readonly store:          Store,
    private readonly sidebarService: SidebarService,
  ) {}

  ngOnInit(): void {
    this.checkScreenSize();

    this.sidebarService.isMobileMenuOpen$
      .pipe(takeUntil(this.destroy$))
      .subscribe((isOpen) => {
        this.isMobileMenuOpen = this.isMobileScreen ? isOpen : true;
      });
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  @HostListener('window:resize')
  onResize(): void {
    this.checkScreenSize();
  }

  closeSidebarOnMobile(): void {
    if (this.isMobileScreen) {
      this.sidebarService.closeMobileMenu();
    }
  }

  private checkScreenSize(): void {
    this.isMobileScreen   = window.innerWidth < 992;
    this.isMobileMenuOpen = !this.isMobileScreen;
  }
}