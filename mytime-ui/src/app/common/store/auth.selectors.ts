import { createFeatureSelector, createSelector } from '@ngrx/store';
import { AuthState } from './auth.state';

// ── Feature selector ───────────────────────────────────────────────────────
export const selectAuthState = createFeatureSelector<AuthState>('auth');

// ── Primitive selectors ────────────────────────────────────────────────────
export const selectCurrentUser = createSelector(
  selectAuthState,
  (state) => state.user
);

export const selectToken = createSelector(
  selectAuthState,
  (state) => state.token
);

export const selectAuthLoading = createSelector(
  selectAuthState,
  (state) => state.loading
);

export const selectAuthError = createSelector(
  selectAuthState,
  (state) => state.error
);

// ── Derived selectors ──────────────────────────────────────────────────────
export const selectIsAuthenticated = createSelector(
  selectAuthState,
  (state) => !!state.token && !!state.user
);

export const selectIsAdmin = createSelector(
  selectCurrentUser,
  (user) => user?.roleId === 1000 || user?.roleId === 1001
);

export const selectIsAdministrator = createSelector(
  selectCurrentUser,
  (user) => user?.roleId === 1000
);

export const selectIsRegularAdmin = createSelector(
  selectCurrentUser,
  (user) => user?.roleId === 1001
);

export const selectUserRoleName = createSelector(
  selectCurrentUser,
  (user) => {
    switch (user?.roleId) {
      case 1000: return 'administrator';
      case 1001: return 'admin';
      default:   return 'user';
    }
  }
);

// ── Composite selectors (used in templates) ────────────────────────────────
export const selectAuthStatus = createSelector(
  selectIsAuthenticated,
  selectAuthLoading,
  (isAuthenticated, isLoading) => ({ isAuthenticated, isLoading })
);

export const selectUserContext = createSelector(
  selectIsAuthenticated,
  selectCurrentUser,
  selectIsAdmin,
  selectIsAdministrator,
  selectIsRegularAdmin,
  selectUserRoleName,
  (isAuthenticated, user, isAdmin, isAdministrator, isRegularAdmin, userRoleName) => ({
    isAuthenticated,
    user,
    isAdmin,
    isAdministrator,
    isRegularAdmin,
    userRoleName,
  })
);