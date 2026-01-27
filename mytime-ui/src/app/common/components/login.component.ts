import { Component, OnInit, OnDestroy, Inject, PLATFORM_ID } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { isPlatformBrowser } from '@angular/common';
import { AccountService } from '../../common/services/account.service';
import { LoaderService } from '../../common/services/loader.service';
import { CommonModule } from '@angular/common';
import { Subject } from 'rxjs';
import { takeUntil } from 'rxjs/operators';
import { TogglePasswordDirective } from '../../common/directives/toggle-password.directive';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    RouterModule, // Add RouterModule for routerLink if needed
    TogglePasswordDirective
  ],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit, OnDestroy {
  loginForm: FormGroup;
  errorMessage = '';
  isDevelopment = true;
  private isBrowser: boolean;
  private destroy$ = new Subject<void>();

  constructor(
    private accountService: AccountService,
    public loaderService: LoaderService,
    private fb: FormBuilder,
    private router: Router,
    @Inject(PLATFORM_ID) platformId: Object
  ) {
    this.isBrowser = isPlatformBrowser(platformId);

    this.loginForm = this.fb.group({
      username: ['', [Validators.required, Validators.minLength(3)]],
      password: ['', [Validators.required, Validators.minLength(6)]],
      rememberMe: [false]
    });
  }

  ngOnInit(): void {
    this.loaderService.show();
    // If already authenticated, redirect based on role
    if (this.accountService.isAuthenticated()) {
      this.accountService.redirectBasedOnRole();
    }

    // Pre-fill username if remembered - SAFE ACCESS
    if (this.isBrowser) {
      const rememberedUsername = localStorage.getItem('rememberedUsername');
      if (rememberedUsername) {
        this.loginForm.patchValue({
          username: rememberedUsername,
          rememberMe: true
        });
      }
    }
    this.loaderService.hide();
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  onSubmit(): void {
    if (this.loginForm.invalid) {
      this.markFormGroupTouched(this.loginForm);
      this.errorMessage = 'Please fill in all required fields correctly';
      return;
    }

    this.errorMessage = '';

    // Handle remember me - SAFE ACCESS
    const rememberMe = this.loginForm.get('rememberMe')?.value;
    if (this.isBrowser) {
      if (rememberMe) {
        localStorage.setItem('rememberedUsername', this.loginForm.get('username')?.value);
      } else {
        localStorage.removeItem('rememberedUsername');
      }
    }

    const credentials = {
      username: this.loginForm.get('username')?.value.trim(),
      password: this.loginForm.get('password')?.value
    };

    // Show loader in main panel (will appear after successful login)
    this.loaderService.show();

    this.accountService.login(credentials)
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (success) => {
          this.loaderService.hide();
          if (!success) {
            this.errorMessage = 'Invalid username or password';
            // Clear password field for security
            this.loginForm.get('password')?.reset();
            // Add shake animation
            this.shakeForm();
          }
          if (success) {
            this.accountService.redirectBasedOnRole();
          }
        },
        error: (error) => {
          this.loaderService.hide();
          this.errorMessage = this.getErrorMessage(error);
          console.error('Login error:', error);
          // Clear password field for security
          this.loginForm.get('password')?.reset();
          this.shakeForm();
        }
      });
  }

  private getErrorMessage(error: any): string {
    if (error.status === 401) {
      return 'Invalid username or password';
    } else if (error.status === 0) {
      return 'Unable to connect to server. Please check your connection.';
    } else if (error.status === 500) {
      return 'Server error. Please try again later.';
    } else if (error.status === 404) {
      return 'Service not found. Please contact administrator.';
    } else if (error.status === 403) {
      return 'Access forbidden. Please check your credentials.';
    }
    return 'An error occurred. Please try again.';
  }

  private markFormGroupTouched(formGroup: FormGroup): void {
    Object.values(formGroup.controls).forEach(control => {
      control.markAsTouched();
      if (control instanceof FormGroup) {
        this.markFormGroupTouched(control);
      }
    });
  }

  private shakeForm(): void {
    // Only shake form in browser environment
    if (this.isBrowser) {
      const formElement = document.querySelector('.auth-form-transparent');
      if (formElement) {
        formElement.classList.add('shake-animation');
        setTimeout(() => {
          formElement.classList.remove('shake-animation');
        }, 500);
      }
    }
  }

  // Convenience getters for template
  get username() { return this.loginForm.get('username'); }
  get password() { return this.loginForm.get('password'); }
  get rememberMe() { return this.loginForm.get('rememberMe'); }

  // Check if field has error
  hasError(controlName: string, errorType: string): boolean {
    const control = this.loginForm.get(controlName);
    return control ? control.hasError(errorType) && (control.dirty || control.touched) : false;
  }

  // Public method for register link
  onRegister(): void {
    // Navigate to registration page
    this.router.navigate(['/register']);
  }

  // Public method for forgot password
  onForgotPassword(): void {
    // Navigate to forgot password page
    this.router.navigate(['/forgot-password']);
  }

  // Public method for social login
  onSocialLogin(provider: string): void {
    this.loaderService.show(`Connecting with ${provider}...`);
    // Implement social login logic
    setTimeout(() => {
      this.loaderService.hide();
      this.errorMessage = `${provider} login is not implemented yet`;
    }, 1500);
  }

  // Quick login for demo purposes (optional)
  quickLogin(username: string, password: string): void {
    this.loginForm.patchValue({ username, password });
    this.onSubmit();
  }
}