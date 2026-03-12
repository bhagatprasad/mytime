import { Injectable } from '@angular/core';
import { CanActivate, Router, ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';
import { Store } from '@ngrx/store';
import { take, map } from 'rxjs/operators';
import { Observable } from 'rxjs';

import { AccountService } from '../services/account.service';
import { selectIsAuthenticated } from '../store/auth.selectors';

/**
 * Protects /user/** routes.
 *
 * Rules:
 *  - Not authenticated  → save attempted URL → redirect to /login
 *  - Authenticated + regular user (roleId 1002) → allow ✅
 *  - Authenticated + admin (roleId 1000 or 1001) → redirect to /admin/dashboard
 *
 * Reads state from NgRx Store — never touches storage.
 */
@Injectable({ providedIn: 'root' })
export class UserGuard implements CanActivate {

  constructor(
    private readonly store:          Store,
    private readonly router:         Router,
    private readonly accountService: AccountService,
  ) {}

  canActivate(
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot
  ): Observable<boolean> {
    return this.store.select(selectIsAuthenticated).pipe(
      take(1),
      map((isAuthenticated) => {
        if (!isAuthenticated) {
          // Save the attempted URL so we can redirect back after login
          this.accountService.redirectUrl = state.url;
          this.router.navigate(['/login']);
          return false;
        }

        // Admins should not access user routes — redirect to admin dashboard
        if (this.accountService.isAdmin()) {
          this.router.navigate(['/admin/dashboard']);
          return false;
        }

        return true;
      })
    );
  }
}