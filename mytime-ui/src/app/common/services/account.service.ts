import { Injectable } from '@angular/core';
import { Store } from '@ngrx/store';
import { Observable } from 'rxjs';
import { take } from 'rxjs/operators';
import { ApplicationUser } from '../models/application-user';
import { selectAuthError, selectAuthLoading, selectCurrentUser, selectIsAdmin, selectIsAuthenticated, selectIsRegularAdmin, selectIsAdministrator, selectUserContext, selectUserRoleName, selectAuthStatus, selectToken } from '../store/auth.selectors';
import * as AuthActions from '../store/auth.actions';
/**
 * AccountService is a thin facade over the NgRx Store.
 *
 * - Components and guards interact with this service (not the Store directly)
 * - This keeps the same public API your existing code already uses
 * - All state lives in the Store; this service never reads/writes storage
 */
@Injectable({ providedIn: 'root' })
export class AccountService {

  // ── Public observables ─────────────────────────────────────────────────

  /** Emits true/false when auth state changes */
  readonly isAuthenticated$: Observable<boolean> =
    this.store.select(selectIsAuthenticated);

  /** Alias kept for any component still using the old name */
  readonly authenticationState$ = this.isAuthenticated$;

  /** Emits { isAuthenticated, isLoading } */
  readonly authStatus$ = this.store.select(selectAuthStatus);

  /** Emits the current ApplicationUser or null */
  readonly currentUser$: Observable<ApplicationUser | null> =
    this.store.select(selectCurrentUser);

  /** Composite context used by app shell, sidebar, header */
  readonly userContext$ = this.store.select(selectUserContext);

  /** Emits true while login API call is in-flight */
  readonly loading$: Observable<boolean> =
    this.store.select(selectAuthLoading);

  /** Emits the latest login error message, or null */
  readonly error$: Observable<string | null> =
    this.store.select(selectAuthError);

  /** Optional redirect URL set by AuthGuard before navigating to /login */
  public redirectUrl: string | null = null;

  constructor(private readonly store: Store) {}

  // ── Actions ────────────────────────────────────────────────────────────

  /**
   * Dispatches the login action.
   * AuthEffects handles the API calls, session persistence, and redirect.
   */
  login(credentials: { username: string; password: string }): void {
    this.store.dispatch(AuthActions.login(credentials));
  }

  /**
   * Dispatches the logout action.
   * AuthEffects clears sessionStorage and navigates to /login.
   */
  logout(): void {
    this.store.dispatch(AuthActions.logout());
  }

  // ── Synchronous snapshot reads (for guards & interceptors) ─────────────

  /**
   * Synchronous check — reads current Store state snapshot.
   * Use the observable isAuthenticated$ in templates/components instead.
   */
  isAuthenticated(): boolean {
    let value = false;
    this.store.select(selectIsAuthenticated).pipe(take(1)).subscribe((v) => (value = v));
    return value;
  }

  /**
   * Returns the current user synchronously from Store snapshot.
   * Use currentUser$ in templates/components instead.
   */
  getCurrentUser(): ApplicationUser | null {
    let user: ApplicationUser | null = null;
    this.store.select(selectCurrentUser).pipe(take(1)).subscribe((u) => (user = u));
    return user;
  }

  /**
   * Returns the JWT token synchronously.
   * Used by the HTTP interceptor to attach Authorization header.
   */
  getAccessToken(): string | null {
    let token: string | null = null;
    this.store.select(selectToken).pipe(take(1)).subscribe((t) => (token = t));
    return token;
  }

  // ── Role helpers ───────────────────────────────────────────────────────

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
        default:   return 'user';
      }
    }
    let name = 'user';
    this.store.select(selectUserRoleName).pipe(take(1)).subscribe((v) => (name = v));
    return name;
  }

  getDefaultDashboard(): string {
    return this.isAdmin() ? '/admin/dashboard' : '/user/dashboard';
  }

  /**
   * Kept for backward compatibility.
   * Redirect logic is now handled by AuthEffects.redirectAfterLogin$.
   */
  redirectBasedOnRole(): void {
    // No-op: effects handle redirect automatically after loginSuccess
  }

  clearRedirectUrl(): void {
    this.redirectUrl = null;
  }
}