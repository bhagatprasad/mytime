// guards/user.guard.ts
import { Injectable } from '@angular/core';
import { CanActivate, Router, ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';
import { AccountService } from '../services/account.service';

@Injectable({
  providedIn: 'root'
})
export class UserGuard implements CanActivate {
  constructor(
    private accountService: AccountService,
    private router: Router
  ) {}

  canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): boolean {
    // Check if user is authenticated
    if (!this.accountService.isAuthenticated()) {
      this.accountService.redirectUrl = state.url;
      this.router.navigate(['/login']);
      return false;
    }

    // Check if user is NOT admin (regular user)
    if (!this.accountService.isAdmin()) {
      return true; // Allow regular users
    }

    // Admins should be redirected to admin dashboard
    this.router.navigate(['/app-admin-dashboard']);
    return false;
  }
}