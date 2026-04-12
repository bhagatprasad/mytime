import { createAction, props } from '@ngrx/store';
import { ApplicationUser } from "../models/application-user";

export const login = createAction(
  '[Login Page] Login',
  props<{ username: string; password: string }>()
);

export const loginSuccess = createAction(
  '[Auth API] Login Success',
  props<{ user: ApplicationUser; token: string }>()
);

export const loginFailure = createAction(
  '[Auth API] Login Failure',
  props<{ error: string }>()
);

export const logout = createAction('[Auth] Logout');