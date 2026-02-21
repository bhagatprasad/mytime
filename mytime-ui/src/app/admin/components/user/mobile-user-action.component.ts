// mobile-user-action.component.ts
import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { ICellRendererAngularComp } from 'ag-grid-angular';

@Component({
  selector: 'app-mobile-user-action',
  imports: [CommonModule],
  standalone: true,
  template: `
    <div class="d-flex justify-content-center gap-2">
      <!-- Details Icon - Always show -->
      <i class="mdi mdi-eye text-info mobile-action-icon" 
         title="View Details" 
         (click)="onDetailsClick($event)"></i>
      
      <!-- Edit Icon - Always show -->
      <i class="mdi mdi-pencil text-primary mobile-action-icon" 
         title="Edit User" 
         (click)="onEditClick($event)"></i>
      
      <!-- Change Password Icon - Always show -->
      <i class="mdi mdi-key-change text-warning mobile-action-icon" 
         title="Change Password" 
         (click)="onChangePasswordClick($event)"></i>
      
      <!-- Status Toggle (Active/Inactive) -->
      <i *ngIf="params.data.IsActive" 
         class="mdi mdi-toggle-switch text-success mobile-action-icon" 
         title="Active - Tap to deactivate" 
         (click)="onDeactivateClick($event)"></i>
      
      <i *ngIf="!params.data.IsActive" 
         class="mdi mdi-toggle-switch-off text-warning mobile-action-icon" 
         title="Inactive - Tap to activate" 
         (click)="onActivateClick($event)"></i>
      
      <!-- Delete Icon - Only for inactive users -->
      <i *ngIf="!params.data.IsActive" 
         class="mdi mdi-delete text-danger mobile-action-icon" 
         title="Delete User" 
         (click)="onDeleteClick($event)"></i>
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
    
    .mobile-action-icon:active {
      transform: scale(0.95);
      background-color: rgba(0, 0, 0, 0.1);
    }
    
    .text-info:hover { color: #138496 !important; }
    .text-primary:hover { color: #0056b3 !important; }
    .text-success:hover { color: #1e7e34 !important; }
    .text-warning:hover { color: #d39e00 !important; }
    .text-danger:hover { color: #bd2130 !important; }
    
    @media (max-width: 768px) {
      .mobile-action-icon {
        padding: 8px;
        font-size: 24px;
      }
    }
  `]
})
export class MobileUserActionComponent implements ICellRendererAngularComp {
  params: any;

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

  onChangePasswordClick(event: MouseEvent): void {
    event.stopPropagation();
    if (this.params.onChangePasswordClick) {
      this.params.onChangePasswordClick(this.params.data);
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