import { HttpInterceptorFn } from '@angular/common/http';

export const apiInterceptor: HttpInterceptorFn = (req, next) => {
  // 1. Get token from localStorage
  const accessToken = localStorage.getItem('AccessToken');
  
  // 2. Only modify requests that don't already have a full URL
  let requestUrl = req.url;
  if (!requestUrl.startsWith('http')) {
    // Remove any accidental double slashes
    requestUrl = requestUrl.replace(/^\/+/, '');
  }

  // 3. Clone request with proper headers
  const authReq = req.clone({
    setHeaders: {
      ...(accessToken ? { 'Authorization': `${accessToken}` } : {}),
      'Content-Type': 'application/json'
    },
    url: requestUrl  // Use the cleaned URL
  });

  console.log('Processed request:', authReq);  // Debug log
  return next(authReq);
};