// employee-action.component.ts - Simplified version
import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { ICellRendererAngularComp } from 'ag-grid-angular';

@Component({
  selector: 'app-employee-action',
  imports: [CommonModule],
  standalone: true,
  template: `
    <div class="d-flex justify-content-center gap-2">
      <!-- Details Icon - Always show -->
      <i class="mdi mdi-eye text-info action-icon" 
         title="View Details" 
         (click)="onDetailsClick($event)"></i>
      
      <!-- User Access Icon - ONLY show if UserId doesn't exist -->
      <i *ngIf="!hasUserAccount" 
         class="mdi mdi-account-key text-primary action-icon" 
         title="Create User Access" 
         (click)="onCreateUserClick($event)"></i>
      
      <!-- DON'T show the user exists checkmark at all - as per requirement -->
      <!-- Remove this block entirely -->
      <!-- <i *ngIf="hasUserAccount" 
         class="mdi mdi-account-check text-success action-icon" 
         title="User Account Exists"></i> -->
      
      <!-- Active/Inactive Toggle - Only show if user exists (hasUserAccount) -->
      <ng-container *ngIf="hasUserAccount">
        <i *ngIf="params.data.IsActive" 
           class="mdi mdi-account-cancel text-warning action-icon" 
           title="Deactivate Employee" 
           (click)="onDeactivateClick($event)"></i>
        
        <i *ngIf="!params.data.IsActive" 
           class="mdi mdi-account-check text-success action-icon" 
           title="Activate Employee" 
           (click)="onActivateClick($event)"></i>
      </ng-container>
      
      <!-- Delete Icon - Only for inactive employees and user exists -->
      <i *ngIf="hasUserAccount && !params.data.IsActive" 
         class="mdi mdi-delete text-danger action-icon" 
         title="Delete" 
         (click)="onDeleteClick($event)"></i>
    </div>
  `,
  styles: [`
    .action-icon {
      cursor: pointer;
      font-size: 20px;
      padding: 4px;
      border-radius: 4px;
      transition: all 0.2s ease;
    }
    
    .action-icon:hover {
      transform: scale(1.2);
      background-color: rgba(0, 0, 0, 0.05);
    }
    
    .text-info:hover { color: #138496 !important; }
    .text-success:hover { color: #1e7e34 !important; }
    .text-primary:hover { color: #0056b3 !important; }
    .text-warning:hover { color: #d39e00 !important; }
    .text-danger:hover { color: #bd2130 !important; }
  `]
})
export class EmployeeActionComponent implements ICellRendererAngularComp {
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

  onDeleteClick(event: MouseEvent): void {
    event.stopPropagation();
    if (this.params.onDeleteClick) {
      this.params.onDeleteClick(this.params.data);
    }
  }
}