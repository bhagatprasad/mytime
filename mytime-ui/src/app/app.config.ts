import { ApplicationConfig, isDevMode } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideHttpClient, withFetch, withInterceptors } from '@angular/common/http';
import { provideAnimations } from '@angular/platform-browser/animations';
import { provideToastr } from 'ngx-toastr';
import { provideStore } from '@ngrx/store';
import { provideEffects } from '@ngrx/effects';
import { provideStoreDevtools } from '@ngrx/store-devtools';
import { provideRouterStore } from '@ngrx/router-store';

import { routes } from './app.routes';
import { apiInterceptor } from './common/interceptors/api.interceptor';
import { authReducer } from './common/store/auth.reducer';
import { metaReducers } from './common/store/auth.meta-reducer';
import { AuthEffects } from './common/store/auth.effects';

// Import profile image feature
import { profileImageReducer } from './common/store/profile-image/profile-image.reducer';
import { ProfileImageEffects } from './common/store/profile-image/profile-image.effects';

export const appConfig: ApplicationConfig = {
  providers: [
    provideRouter(routes),
    provideHttpClient(
      withFetch(),
      withInterceptors([apiInterceptor])
    ),
    provideAnimations(),
    provideToastr({
      timeOut: 3000,
      positionClass: 'toast-top-center',
      preventDuplicates: true,
      closeButton: true,
      progressBar: true,
    }),
    // Register ALL reducers here
    provideStore(
      { 
        auth: authReducer,
        profileImage: profileImageReducer  // ← Add this line
      },
      { metaReducers }
    ),
    // Register ALL effects here
    provideEffects([
      AuthEffects,
      ProfileImageEffects  // ← Add this line
    ]),
    provideStoreDevtools({
      maxAge: 25,
      logOnly: !isDevMode(),
      connectInZone: true,
    }),
    provideRouterStore(),
  ],
};