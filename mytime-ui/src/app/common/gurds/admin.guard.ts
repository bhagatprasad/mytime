import { Injectable } from '@angular/core';
import { CanActivate, Router } from '@angular/router';
import { Store } from '@ngrx/store';
import { take, map } from 'rxjs/operators';
import { Observable, combineLatest } from 'rxjs';
import { selectIsAuthenticated, selectIsAdmin } from '../store/auth.selectors';

/**
 * Protects /admin/** routes.
 *
 * Rules:
 *  - Not authenticated              → redirect to /login
 *  - Authenticated + not admin      → redirect to /user/dashboard
 *  - Authenticated + admin          → allow ✅
 *
 * Reads state from NgRx Store — never touches storage.
 */
@Injectable({ providedIn: 'root' })
export class AdminGuard implements CanActivate {

  constructor(
    private readonly store:  Store,
    private readonly router: Router,
  ) {}

  canActivate(): Observable<boolean> {
    return combineLatest([
      this.store.select(selectIsAuthenticated),
      this.store.select(selectIsAdmin),
    ]).pipe(
      take(1),
      map(([isAuthenticated, isAdmin]) => {
        if (!isAuthenticated) {
          this.router.navigate(['/login']);
          return false;
        }

        if (!isAdmin) {
          // Authenticated but not an admin — redirect to user area
          this.router.navigate(['/user/dashboard']);
          return false;
        }

        return true;
      })
    );
  }
}