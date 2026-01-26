import { ApplicationConfig } from '@angular/core';
import { provideRouter } from '@angular/router';
import { routes } from './app.routes';
import { provideHttpClient, withFetch, withInterceptors } from '@angular/common/http';
import { provideAnimations } from '@angular/platform-browser/animations';
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
    
    // Animations (required for toastr if you use it later)
    provideAnimations(),
  ]
};