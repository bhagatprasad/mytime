import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class LoaderService {
  private isLoading = new BehaviorSubject<boolean>(false);
  private message = new BehaviorSubject<string>('Loading...');
  
  isLoading$ = this.isLoading.asObservable();
  message$ = this.message.asObservable();

  // Show loader with optional message
  show(message?: string) {
    if (message) {
      this.message.next(message);
    }
    this.isLoading.next(true);
  }

  // Hide loader
  hide() {
    this.isLoading.next(false);
  }

  // Update message while loader is showing
  updateMessage(message: string) {
    this.message.next(message);
  }
}