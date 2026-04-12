import { HttpInterceptorFn } from '@angular/common/http';

export const apiInterceptor: HttpInterceptorFn = (req, next) => {
  const accessToken = localStorage.getItem('AccessToken');
  
  let requestUrl = req.url;
  if (!requestUrl.startsWith('http')) {
    requestUrl = requestUrl.replace(/^\/+/, '');
  }

  const authReq = req.clone({
    setHeaders: {
      ...(accessToken ? { 'Authorization': `Bearer ${accessToken}` } : {}),
      'Content-Type': 'application/json'
    },
    url: requestUrl
  });
  
  return next(authReq);
};