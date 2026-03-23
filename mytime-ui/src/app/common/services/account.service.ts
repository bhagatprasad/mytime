import { Injectable } from '@angular/core';
import { Store } from '@ngrx/store';
import { Observable } from 'rxjs';
import { take } from 'rxjs/operators';
import { ApplicationUser } from '../models/application-user';
import { selectAuthError, selectAuthLoading, selectCurrentUser, selectIsAdmin, selectIsAuthenticated, selectIsRegularAdmin, selectIsAdministrator, selectUserContext, selectUserRoleName, selectAuthStatus, selectToken } from '../store/auth.selectors';
import * as AuthActions from '../store/auth.actions';

@Injectable({ providedIn: 'root' })
export class AccountService {

  readonly isAuthenticated$: Observable<boolean> = this.store.select(selectIsAuthenticated);

  readonly authenticationState$ = this.isAuthenticated$;

  readonly authStatus$ = this.store.select(selectAuthStatus);

  readonly currentUser$: Observable<ApplicationUser | null> = this.store.select(selectCurrentUser);

  readonly userContext$ = this.store.select(selectUserContext);

  readonly loading$: Observable<boolean> = this.store.select(selectAuthLoading);

  readonly error$: Observable<string | null> = this.store.select(selectAuthError);

  public redirectUrl: string | null = null;

  constructor(private readonly store: Store) { }

  login(credentials: { username: string; password: string }): void {
    this.store.dispatch(AuthActions.login(credentials));
  }

  logout(): void {
    this.store.dispatch(AuthActions.logout());
  }

  isAuthenticated(): boolean {
    let value = false;
    this.store.select(selectIsAuthenticated).pipe(take(1)).subscribe((v) => (value = v));
    return value;
  }

  getCurrentUser(): ApplicationUser | null {
    let user: ApplicationUser | null = null;
    this.store.select(selectCurrentUser).pipe(take(1)).subscribe((u) => (user = u));
    return user;
  }


  getAccessToken(): string | null {
    let token: string | null = null;
    this.store.select(selectToken).pipe(take(1)).subscribe((t) => (token = t));
    return token;
  }

  isAdmin(user?: ApplicationUser): boolean {
    if (user) return user.roleId === 1000 || user.roleId === 1001;
    let value = false;
    this.store.select(selectIsAdmin).pipe(take(1)).subscribe((v) => (value = v));
    return value;
  }

  isAdministrator(user?: ApplicationUser): boolean {
    if (user) return user.roleId === 1000;
    let value = false;
    this.store.select(selectIsAdministrator).pipe(take(1)).subscribe((v) => (value = v));
    return value;
  }

  isRegularAdmin(user?: ApplicationUser): boolean {
    if (user) return user.roleId === 1001;
    let value = false;
    this.store.select(selectIsRegularAdmin).pipe(take(1)).subscribe((v) => (value = v));
    return value;
  }

  hasRole(roleId: number): boolean {
    return this.getCurrentUser()?.roleId === roleId;
  }

  getUserRoleName(user?: ApplicationUser): string {
    if (user) {
      switch (user.roleId) {
        case 1000: return 'administrator';
        case 1001: return 'admin';
        default: return 'user';
      }
    }
    let name = 'user';
    this.store.select(selectUserRoleName).pipe(take(1)).subscribe((v) => (name = v));
    return name;
  }

  getDefaultDashboard(): string {
    return this.isAdmin() ? '/admin/dashboard' : '/user/dashboard';
  }

  redirectBasedOnRole(): void {

  }

  clearRedirectUrl(): void {
    this.redirectUrl = null;
  }
}