// mobile-employee-action.component.ts
import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { ICellRendererAngularComp } from 'ag-grid-angular';

@Component({
  selector: 'app-mobile-employee-action',
  imports: [CommonModule],
  standalone: true,
  template: `
    <div class="d-flex justify-content-center gap-2">
      <!-- Details Icon - Always show -->
      <i class="mdi mdi-eye text-info mobile-action-icon" 
         title="View Details" 
         (click)="onDetailsClick($event)"></i>
      
      <!-- User Access Icon - ONLY show if UserId doesn't exist -->
      <i *ngIf="!hasUserAccount" 
         class="mdi mdi-account-key text-primary mobile-action-icon" 
         title="Create User" 
         (click)="onCreateUserClick($event)"></i>
      
      <!-- DON'T show user exists checkmark icon at all -->
      <!-- Remove this block -->
      <!-- <i *ngIf="hasUserAccount" 
         class="mdi mdi-account-check text-success mobile-action-icon" 
         title="User Exists"></i> -->
      
      <!-- Status Toggle (Active/Inactive) - Only show if user exists -->
      <ng-container *ngIf="hasUserAccount">
        <i *ngIf="params.data.IsActive" 
           class="mdi mdi-toggle-switch text-success mobile-action-icon" 
           title="Active - Tap to deactivate" 
           (click)="onDeactivateClick($event)"></i>
        
        <i *ngIf="!params.data.IsActive" 
           class="mdi mdi-toggle-switch-off text-warning mobile-action-icon" 
           title="Inactive - Tap to activate" 
           (click)="onActivateClick($event)"></i>
      </ng-container>
    </div>
  `,
  styles: [`
    .mobile-action-icon {
      cursor: pointer;
      font-size: 22px;
      padding: 6px;
      border-radius: 6px;
      transition: all 0.2s ease;
    }
    
    .mobile-action-icon:hover {
      transform: scale(1.1);
      background-color: rgba(0, 0, 0, 0.05);
    }
    
    /* For touch devices */
    .mobile-action-icon:active {
      transform: scale(0.95);
      background-color: rgba(0, 0, 0, 0.1);
    }
    
    .text-info:hover { color: #138496 !important; }
    .text-success:hover { color: #1e7e34 !important; }
    .text-primary:hover { color: #0056b3 !important; }
    .text-warning:hover { color: #d39e00 !important; }
    
    /* Remove the non-clickable icon styles since we removed that icon */
    /* .mdi-account-check[title="User Exists"] {
      cursor: default !important;
      opacity: 0.7;
    }
    .mdi-account-check[title="User Exists"]:hover {
      transform: none;
      background-color: transparent;
    } */
    
    /* Larger touch targets for mobile */
    @media (max-width: 768px) {
      .mobile-action-icon {
        padding: 8px;
        font-size: 24px;
      }
    }
  `]
})
export class MobileEmployeeActionComponent implements ICellRendererAngularComp {
  params: any;

  // Check if user account exists based on UserId
  get hasUserAccount(): boolean {
    const userId = this.params.data.UserId;
    // Check if UserId exists and is a positive number
    return userId !== null && userId !== undefined && userId > 0;
  }

  agInit(params: any): void {
    this.params = params;
  }

  refresh(params: any): boolean {
    this.params = params;
    return true;
  }

  onDetailsClick(event: MouseEvent): void {
    event.stopPropagation();
    if (this.params.onDetailsClick) {
      this.params.onDetailsClick(this.params.data);
    }
  }

  onEditClick(event: MouseEvent): void {
    event.stopPropagation();
    if (this.params.onEditClick) {
      this.params.onEditClick(this.params.data);
    }
  }

  onCreateUserClick(event: MouseEvent): void {
    event.stopPropagation();
    if (this.params.onCreateUserClick) {
      this.params.onCreateUserClick(this.params.data);
    }
  }

  onActivateClick(event: MouseEvent): void {
    event.stopPropagation();
    if (this.params.onActivateClick) {
      this.params.onActivateClick(this.params.data);
    }
  }

  onDeactivateClick(event: MouseEvent): void {
    event.stopPropagation();
    if (this.params.onDeactivateClick) {
      this.params.onDeactivateClick(this.params.data);
    }
  }
}