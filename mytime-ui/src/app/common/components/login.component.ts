import { Component, OnInit, OnDestroy, inject } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { Store } from '@ngrx/store';
import { Subject } from 'rxjs';
import { filter, takeUntil } from 'rxjs/operators';

import { LoaderService } from '../../common/services/loader.service';
import { NotifyService } from '../services/notify.service';
import { TogglePasswordDirective } from '../../common/directives/toggle-password.directive';
import { selectAuthError, selectAuthLoading, selectIsAuthenticated } from '../../common/store/auth.selectors';
import * as AuthActions from '../../common/store/auth.actions';
import { AccountService } from '../../common/services/account.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    RouterModule,
    TogglePasswordDirective,
  ],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],
})
export class LoginComponent implements OnInit, OnDestroy {

  loginForm: FormGroup;
  private readonly destroy$ = new Subject<void>();

  readonly loading$ = this.store.select(selectAuthLoading);
  readonly error$   = this.store.select(selectAuthError);

  constructor(
    private readonly store:   Store,
    private readonly fb:      FormBuilder,
    private readonly router:  Router,
    private readonly toaster: NotifyService,
    public  readonly loaderService: LoaderService,
  ) {
    this.loginForm = this.fb.group({
      username: ['', [Validators.required, Validators.minLength(3)]],
      password: ['', [Validators.required, Validators.minLength(6)]],
    });
  }

  ngOnInit(): void {
    this.store.select(selectIsAuthenticated).pipe(
      filter((isAuth) => isAuth),
      takeUntil(this.destroy$)
    ).subscribe(() => {
      const accountService = inject(AccountService);
      this.router.navigate([accountService.getDefaultDashboard()]);
    });

    this.error$.pipe(
      filter((err): err is string => !!err),
      takeUntil(this.destroy$)
    ).subscribe((err) => {
      this.toaster.showError(err);
      this.loginForm.get('password')?.reset();
      this.shakeForm();
    });
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  onSubmit(): void {
    if (this.loginForm.invalid) {
      this.markAllTouched(this.loginForm);
      this.toaster.showError('Please fill in all required fields correctly');
      return;
    }

    const { username, password } = this.loginForm.value;

    this.store.dispatch(
      AuthActions.login({ username: username.trim(), password })
    );
  }

  get username() { return this.loginForm.get('username'); }
  get password() { return this.loginForm.get('password'); }

  hasError(controlName: string, errorType: string): boolean {
    const control = this.loginForm.get(controlName);
    return !!control?.hasError(errorType) && (control.dirty || control.touched);
  }

  onForgotPassword(): void { this.router.navigate(['/forgot-password']); }
  onRegister():       void { this.router.navigate(['/register']);         }

  private markAllTouched(group: FormGroup): void {
    Object.values(group.controls).forEach((control) => {
      control.markAsTouched();
      if (control instanceof FormGroup) {
        this.markAllTouched(control);
      }
    });
  }

  private shakeForm(): void {
    const el = document.querySelector('.auth-form-transparent');
    if (!el) return;
    el.classList.add('shake-animation');
    setTimeout(() => el.classList.remove('shake-animation'), 500);
  }
}