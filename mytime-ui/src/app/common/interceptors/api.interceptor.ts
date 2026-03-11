import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { Store } from '@ngrx/store';
import { switchMap, take } from 'rxjs/operators';
import { selectToken } from '../store/auth.selectors';
/**
 * HTTP interceptor that attaches the Bearer token to every outgoing request.
 *
 * Token is read from the NgRx Store via selectToken selector.
 * This interceptor never touches localStorage or sessionStorage directly.
 */
export const apiInterceptor: HttpInterceptorFn = (req, next) => {
  const store = inject(Store);

  return store.select(selectToken).pipe(
    take(1),
    switchMap((token) =>
      next(
        req.clone({
          setHeaders: {
            'Content-Type': 'application/json',
            ...(token ? { Authorization: `Bearer ${token}` } : {}),
          },
        })
      )
    )
  );
};