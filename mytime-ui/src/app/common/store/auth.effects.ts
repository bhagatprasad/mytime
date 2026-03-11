import { Injectable, inject } from '@angular/core';
import { Router } from '@angular/router';
import { Actions, createEffect, ofType } from '@ngrx/effects';
import { Store } from '@ngrx/store';
import { of } from 'rxjs';
import { switchMap, map, catchError, tap, withLatestFrom } from 'rxjs/operators';

import { ApiService } from '../../common/services/api.service';
import { ApplicationUser } from '../../common/models/application-user';
import { selectAuthState } from './auth.selectors';
import * as AuthActions from './auth.actions';

const AUTH_ENDPOINT   = 'auth/AuthenticateUser';
const CLAIMS_ENDPOINT = 'auth/GenarateUserClaims';
const SESSION_KEY     = 'auth_session';

@Injectable()
export class AuthEffects {

  private readonly actions$ = inject(Actions);
  private readonly api      = inject(ApiService);
  private readonly router   = inject(Router);
  private readonly store    = inject(Store);

  // ── Step 1: Authenticate user credentials ─────────────────────────────
  // ── Step 2: Generate user claims from JWT  ─────────────────────────────
  // ── Step 3: Dispatch loginSuccess or loginFailure ──────────────────────
  login$ = createEffect(() =>
    this.actions$.pipe(
      ofType(AuthActions.login),
      switchMap(({ username, password }) =>
        this.api.send<{ jwt_token: string }>('POST', AUTH_ENDPOINT, { username, password }).pipe(
          switchMap((authResponse) =>
            this.api.send<any>('POST', CLAIMS_ENDPOINT, authResponse).pipe(
              map((data) =>
                AuthActions.loginSuccess({
                  token: authResponse.jwt_token,
                  user: this.mapUser(data),
                })
              ),
              catchError((err) =>
                of(AuthActions.loginFailure({
                  error: err?.message ?? 'Failed to load user profile',
                }))
              )
            )
          ),
          catchError((err) =>
            of(AuthActions.loginFailure({
              error: this.httpError(err),
            }))
          )
        )
      )
    )
  );

  // ── Persist session to sessionStorage after successful login ───────────
  // sessionStorage survives refresh but clears when tab closes
  persistSession$ = createEffect(() =>
    this.actions$.pipe(
      ofType(AuthActions.loginSuccess),
      withLatestFrom(this.store.select(selectAuthState)),
      tap(([, { user, token }]) => {
        try {
          sessionStorage.setItem(SESSION_KEY, JSON.stringify({ user, token }));
        } catch {
          // Private browsing / storage quota exceeded — fail silently
        }
      })
    ),
    { dispatch: false }
  );

  // ── Redirect to dashboard based on role after login ───────────────────
  redirectAfterLogin$ = createEffect(() =>
    this.actions$.pipe(
      ofType(AuthActions.loginSuccess),
      withLatestFrom(this.store.select(selectAuthState)),
      tap(([, { user }]) => {
        const isAdmin = user?.roleId === 1000 || user?.roleId === 1001;
        this.router.navigate([isAdmin ? '/admin/dashboard' : '/user/dashboard']);
      })
    ),
    { dispatch: false }
  );

  // ── Clear sessionStorage and redirect to login on logout ──────────────
  logout$ = createEffect(() =>
    this.actions$.pipe(
      ofType(AuthActions.logout),
      tap(() => {
        try {
          sessionStorage.removeItem(SESSION_KEY);
        } catch {
          // Ignore
        }
        this.router.navigate(['/login']);
      })
    ),
    { dispatch: false }
  );

  // ── Helpers ────────────────────────────────────────────────────────────

  private mapUser(data: any): ApplicationUser {
    return {
      id:        data.id?.toString(),
      fullName:  `${data.first_name ?? ''} ${data.last_name ?? ''}`.trim(),
      firstName: data.first_name,
      lastName:  data.last_name,
      email:     data.email,
      phone:     data.phone,
      roleId:    data.role_id,
    };
  }

  private httpError(err: { status?: number }): string {
    switch (err?.status) {
      case 401: return 'Invalid username or password';
      case 0:   return 'Unable to connect to server. Please check your connection.';
      case 403: return 'Access forbidden. Please check your credentials.';
      case 404: return 'Service not found. Please contact administrator.';
      case 500: return 'Server error. Please try again later.';
      default:  return 'An error occurred. Please try again.';
    }
  }
}