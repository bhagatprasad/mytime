// admin.guard.ts - Updated
import { Injectable } from '@angular/core';
import { CanActivate, Router } from '@angular/router';
import { AccountService } from '../services/account.service';

@Injectable({
  providedIn: 'root'
})
export class AdminGuard implements CanActivate {
  constructor(
    private accountService: AccountService,
    private router: Router
  ) {}

  canActivate(): boolean {
    if (this.accountService.isAuthenticated() && this.accountService.isAdmin()) {
      return true;
    }
    
    // Redirect to user dashboard if authenticated but not admin
    if (this.accountService.isAuthenticated()) {
      this.router.navigate(['/app-user-dashboard']);
      return false;
    }
    
    this.router.navigate(['/login']);
    return false;
  }
}

