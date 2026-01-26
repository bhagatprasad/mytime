import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpRequest, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs';
import { filter, map } from 'rxjs/operators';
import { environment } from '../../../environment';


type BodylessMethod = 'GET' | 'HEAD' | 'DELETE' | 'OPTIONS';
type BodyMethod = 'POST' | 'PUT' | 'PATCH';
type HttpMethod = BodylessMethod | BodyMethod;

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  constructor(private http: HttpClient) {}

  send<TResponse>(method: BodylessMethod, url: string): Observable<TResponse>;
  send<TResponse>(method: BodyMethod, url: string, body: any): Observable<TResponse>;
  send<TResponse>(method: HttpMethod, url: string, body?: any): Observable<TResponse> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json'
    });

    // Prepend the base URL to the endpoint
    const fullUrl = `${environment.baseUrl}/${url}`;

    // Create the appropriate request based on method type
    let req: HttpRequest<any>;
    switch (method) {
      case 'GET':
      case 'HEAD':
      case 'DELETE':
      case 'OPTIONS':
        req = new HttpRequest(method, fullUrl, { headers });
        break;
      case 'POST':
      case 'PUT':
      case 'PATCH':
        req = new HttpRequest(method, fullUrl, JSON.stringify(body), { headers });
        break;
      default:
        throw new Error(`Unsupported HTTP method: ${method}`);
    }

    return this.http.request<TResponse>(req).pipe(
      filter(event => event instanceof HttpResponse),
      map(event => {
        const response = event as HttpResponse<TResponse>;
        return this.handleResponse<TResponse>(response);
      })
    );
  }

  private handleResponse<T>(response: HttpResponse<T>): T {
    if (response.status >= 200 && response.status < 300) {
      if (response.body === null && response.status === 204) {
        return true as unknown as T;
      }
      return response.body as T;
    } else {
      console.error('Error response:', response);
      throw new Error(`HTTP error: ${response.status} - ${response.statusText}`);
    }
  }
}