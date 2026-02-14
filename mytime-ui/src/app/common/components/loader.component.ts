import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LoaderService } from '../../common/services/loader.service';

@Component({
  selector: 'app-panel-loader',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="panel-loader-overlay" *ngIf="isLoading">
      <div class="loader-container">
        <!-- Big Spinner -->
        <div class="big-spinner">
          <div class="spinner-ring"></div>
          <div class="spinner-center"></div>
        </div>
        
        <!-- Loading Message -->
        <div class="loader-text">{{ message }}</div>
      </div>
    </div>
  `,
  styles: [`
    .panel-loader-overlay {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(255, 255, 255, 0.85);
      z-index: 999999;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    
    .loader-container {
      text-align: center;
      max-width: 400px;
      width: 100%;
      padding: 20px;
    }
    
    /* Big Spinner - Original Size */
    .big-spinner {
      position: relative;
      width: 120px;
      height: 120px;
      margin: 0 auto 25px;
    }
    
    .spinner-ring {
      width: 100%;
      height: 100%;
      border: 12px solid rgba(0, 123, 255, 0.1);
      border-top: 12px solid #007bff;
      border-radius: 50%;
      animation: spin 1.5s linear infinite;
      box-sizing: border-box;
    }
    
    .spinner-center {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      width: 60px;
      height: 60px;
      border: 6px solid rgba(0, 123, 255, 0.1);
      border-radius: 50%;
      background: white;
      box-sizing: border-box;
    }
    
    @keyframes spin {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }
    
    .loader-text {
      font-size: 18px;
      font-weight: 600;
      color: #333;
      margin-top: 15px;
      text-align: center;
    }
    
    /* Pulse animation for center */
    .spinner-center {
      animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
      0% { 
        transform: translate(-50%, -50%) scale(0.9);
        opacity: 0.8;
      }
      50% { 
        transform: translate(-50%, -50%) scale(1.1);
        opacity: 1;
      }
      100% { 
        transform: translate(-50%, -50%) scale(0.9);
        opacity: 0.8;
      }
    }
  `]
})
export class PanelLoaderComponent implements OnInit {
  isLoading = false;
  message = 'Loading...';

  constructor(private loaderService: LoaderService) {}

  ngOnInit() {
    this.loaderService.isLoading$.subscribe((loading: boolean) => {
      this.isLoading = loading;
    });

    this.loaderService.message$.subscribe((message: string) => {
      this.message = message;
    });
  }
}