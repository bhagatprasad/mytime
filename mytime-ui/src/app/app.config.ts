import { ApplicationConfig } from '@angular/core';
import { provideRouter } from '@angular/router';
import { routes } from './app.routes';
import { provideHttpClient, withFetch, withInterceptors } from '@angular/common/http';
import { provideAnimations } from '@angular/platform-browser/animations';
import { provideToastr } from 'ngx-toastr'; // Add this
import { apiInterceptor } from './common/interceptors/api.interceptor';

export const appConfig: ApplicationConfig = {
  providers: [
    // Router
    provideRouter(routes),
    
    // HTTP Client with interceptors
    provideHttpClient(
      withFetch(),
      withInterceptors([
        apiInterceptor
      ])
    ),
    
    // Animations (required for toastr)
    provideAnimations(),
    
    // Toastr configuration
    provideToastr({
      timeOut: 3000,
      positionClass: 'toast-top-center',
      preventDuplicates: true,
      closeButton: true,
      progressBar: true,
    })
  ]
};