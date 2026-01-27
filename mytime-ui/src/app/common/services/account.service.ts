import { Injectable, PLATFORM_ID, Inject, OnDestroy } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { BehaviorSubject, Observable, Subject } from 'rxjs';
import { filter, distinctUntilChanged, takeUntil, map } from 'rxjs/operators';
import { Router } from '@angular/router';
import { environment } from '../../../environment';
import { AuthResponse } from '../models/auth-response';
import { UserAuthentication } from '../models/user-authentication';
import { ApplicationUser } from '../models/application-user';
import { ApiService } from './api.service';

@Injectable({ providedIn: 'root' })
export class AccountService implements OnDestroy {
    private readonly authEndpoint = 'auth/AuthenticateUser';
    private readonly claimsEndpoint = 'auth/GenarateUserClaims';

    // Role constants based on your data
    private readonly ROLE_IDS = {
        ADMINISTRATOR: 1000,
        ADMIN: 1001,
        USER: 1002 // Assuming regular users have roleId 1002
    };

    private authenticationState = new BehaviorSubject<boolean | null>(null);
    private isBrowser: boolean;
    private inactivityTimer: any;
    private readonly INACTIVITY_TIMEOUT = 30 * 60 * 1000; // 30 minutes
    private destroy$ = new Subject<void>();

    // Add redirectUrl property with proper type
    public redirectUrl: string | null = null; // Start with null

    // Public observable (using $ naming convention)
    authenticationState$ = this.authenticationState.asObservable().pipe(
        filter(state => state !== null),
        distinctUntilChanged()
    );

    constructor(
        private apiService: ApiService,
        private router: Router,
        @Inject(PLATFORM_ID) platformId: Object
    ) {
        this.isBrowser = isPlatformBrowser(platformId);
        this.initializeAuthState();
        this.setupInactivityMonitoring();
    }

    ngOnDestroy(): void {
        this.destroy$.next();
        this.destroy$.complete();
        this.clearInactivityTimer();
    }

    private initializeAuthState(): void {
        if (!this.isBrowser) {
            this.authenticationState.next(false);
            return;
        }

        // Check authentication status
        const isAuth = this.isAuthenticated();
        this.authenticationState.next(isAuth);

        // Auto-redirect if authenticated and on login page
        if (isAuth && this.isLoginPage()) {
            this.redirectBasedOnRole();
        }

        if (isAuth) {
            this.resetInactivityTimer();
        }
    }

    private isLoginPage(): boolean {
        if (!this.isBrowser) return false;
        return window.location.pathname.includes('/login');
    }

    public redirectBasedOnRole(): void {
        const user = this.getCurrentUser();
        if (!user) {
            this.router.navigate(['/login']);
            return;
        }

        // First, check if there's a stored redirect URL that's not a default route
        if (this.redirectUrl &&
            this.redirectUrl !== '/user/dashboard' &&
            this.redirectUrl !== '/admin/dashboard' &&
            this.redirectUrl !== '/app-user-dashboard') {
            const redirectTo = this.redirectUrl;
            this.clearRedirectUrl(); // Clear after use
            this.router.navigateByUrl(redirectTo);
            return;
        }

        // Otherwise, redirect based on role
        const isAdmin = this.isAdmin(user);
        const redirectRoute = isAdmin ? '/admin/dashboard' : '/user/dashboard';
        this.clearRedirectUrl(); // Clear after use
        this.router.navigate([redirectRoute]);
    }

    private setupInactivityMonitoring(): void {
        if (!this.isBrowser) return;

        const events = ['mousemove', 'keypress', 'scroll', 'click', 'touchstart'];
        events.forEach(event => {
            window.addEventListener(event, this.resetInactivityTimer.bind(this));
        });

        // Also monitor visibility change
        document.addEventListener('visibilitychange', () => {
            if (!document.hidden) {
                this.resetInactivityTimer();
            }
        });
    }

    private resetInactivityTimer(): void {
        this.clearInactivityTimer();
        if (this.isAuthenticated()) {
            this.inactivityTimer = setTimeout(
                () => this.logout(),
                this.INACTIVITY_TIMEOUT
            );
        }
    }

    private clearInactivityTimer(): void {
        if (this.inactivityTimer) {
            clearTimeout(this.inactivityTimer);
            this.inactivityTimer = null;
        }
    }

    isAuthenticated(): boolean {
        if (!this.isBrowser) return false;
        return !!this.getAccessToken() && !!this.getCurrentUser();
    }

    // Check if user has admin role (Administrator or Admin)
    isAdmin(user?: ApplicationUser): boolean {
        const currentUser = user || this.getCurrentUser();
        if (!currentUser || !currentUser.roleId) return false;

        // Check if roleId is Administrator (1000) or Admin (1001)
        return currentUser.roleId === this.ROLE_IDS.ADMINISTRATOR ||
            currentUser.roleId === this.ROLE_IDS.ADMIN;
    }

    // Check if user is Administrator specifically
    isAdministrator(user?: ApplicationUser): boolean {
        const currentUser = user || this.getCurrentUser();
        if (!currentUser || !currentUser.roleId) return false;

        return currentUser.roleId === this.ROLE_IDS.ADMINISTRATOR;
    }

    // Check if user is regular Admin (not Administrator)
    isRegularAdmin(user?: ApplicationUser): boolean {
        const currentUser = user || this.getCurrentUser();
        if (!currentUser || !currentUser.roleId) return false;

        return currentUser.roleId === this.ROLE_IDS.ADMIN;
    }

    // Check if user has specific role
    hasRole(roleId: number): boolean {
        const user = this.getCurrentUser();
        return user?.roleId === roleId;
    }

    // Get user's role name
    getUserRoleName(user?: ApplicationUser): string {
        const currentUser = user || this.getCurrentUser();
        if (!currentUser?.roleId) return 'user';

        switch (currentUser.roleId) {
            case this.ROLE_IDS.ADMINISTRATOR:
                return 'administrator';
            case this.ROLE_IDS.ADMIN:
                return 'admin';
            default:
                return 'user';
        }
    }

    // Updated localStorage methods with proper error handling
    private getLocalStorageItem(key: string): string | null {
        try {
            return this.isBrowser ? localStorage.getItem(key) : null;
        } catch {
            return null;
        }
    }

    private setLocalStorageItem(key: string, value: string): void {
        try {
            if (this.isBrowser) {
                localStorage.setItem(key, value);
            }
        } catch (error) {
            console.error('Error setting localStorage item:', error);
        }
    }

    private removeLocalStorageItem(key: string): void {
        try {
            if (this.isBrowser) {
                localStorage.removeItem(key);
            }
        } catch (error) {
            console.error('Error removing localStorage item:', error);
        }
    }

    // Authentication methods
    authenticateUser(userAuthentication: UserAuthentication): Observable<AuthResponse> {
        return this.apiService.send<AuthResponse>('POST', this.authEndpoint, userAuthentication);
    }

    generateUserClaims(authResponse: AuthResponse): Observable<ApplicationUser> {
        return this.apiService.send<any>('POST', this.claimsEndpoint, authResponse).pipe(
            map(data => {
                return {
                    id: data.id?.toString(), 
                    fullName: `${data.first_name || ''} ${data.last_name || ''}`.trim(),
                    firstName: data.first_name,
                    lastName: data.last_name,
                    email: data.email,
                    phone: data.phone,
                    roleId: data.role_id  // Map role_id to role_Id (number)
                } as ApplicationUser;
            }));
    }

    // Login process
    login(userAuthentication: any): Observable<boolean> {
        return new Observable<boolean>(observer => {
            this.authenticateUser(userAuthentication).subscribe({
                next: (authResponse) => {
                    this.generateUserClaims(authResponse).subscribe({
                        next: (user) => {
                            this.storeUserSession(user, authResponse.jwt_token);
                            observer.next(true);
                            observer.complete();
                        },
                        error: (error) => {
                            console.error('Error generating user claims:', error);
                            observer.next(false);
                            observer.complete();
                        }
                    });
                },
                error: (error) => {
                    console.error('Authentication error:', error);
                    observer.next(false);
                    observer.complete();
                }
            });
        });
    }

    storeUserSession(user: ApplicationUser, token: string): void {
        this.setLocalStorageItem('ApplicationUser', JSON.stringify(user));
        this.setLocalStorageItem('AccessToken', token);

        this.authenticationState.next(true);
        this.resetInactivityTimer();

        // Redirect based on user role or stored redirect URL
        this.redirectBasedOnRole();
    }

    logout(): void {
        this.removeLocalStorageItem('ApplicationUser');
        this.removeLocalStorageItem('AccessToken');
        this.authenticationState.next(false);
        this.clearInactivityTimer();
        this.clearRedirectUrl();

        // Navigate to login only if not already there
        if (this.isBrowser && !this.router.url.includes('/login')) {
            this.router.navigate(['/login']);
        }
    }

    // Getters
    getCurrentUser(): ApplicationUser | null {
        try {
            const user = this.getLocalStorageItem('ApplicationUser');
            return user ? JSON.parse(user) : null;
        } catch {
            return null;
        }
    }

    getAccessToken(): string | null {
        return this.getLocalStorageItem('AccessToken');
    }

    // Helper method to clear redirect URL - set to null instead of a default
    clearRedirectUrl(): void {
        this.redirectUrl = null;
    }

    // Helper method to get the default dashboard based on role
    getDefaultDashboard(): string {
        const user = this.getCurrentUser();
        if (!user) return '/login';

        return this.isAdmin(user) ? '/admin/dashboard' : '/user/dashboard';
    }
}