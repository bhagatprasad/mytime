// administrator.guard.ts - For Administrator only access
import { Injectable } from '@angular/core';
import { CanActivate, Router } from '@angular/router';
import { AccountService } from '../services/account.service';

@Injectable({
  providedIn: 'root'
})
export class AdministratorGuard implements CanActivate {
  constructor(
    private accountService: AccountService,
    private router: Router
  ) {}

  canActivate(): boolean {
    if (this.accountService.isAuthenticated() && this.accountService.isAdministrator()) {
      return true;
    }
    
    // Redirect to appropriate dashboard
    if (this.accountService.isAuthenticated()) {
      if (this.accountService.isRegularAdmin()) {
        this.router.navigate(['/app-admin-dashboard']);
      } else {
        this.router.navigate(['/app-user-dashboard']);
      }
      return false;
    }
    
    this.router.navigate(['/login']);
    return false;
  }
}