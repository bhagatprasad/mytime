import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { ICellRendererAngularComp } from 'ag-grid-angular';

@Component({
  selector: 'app-user-action',
  imports: [CommonModule],
  standalone: true,
  template: `
    <div class="d-flex justify-content-center gap-2">
      <!-- Details Icon - Always show -->
      <i class="mdi mdi-eye text-info action-icon" 
         title="View Details" 
         (click)="onDetailsClick($event)"></i>
      
      <!-- Edit Icon - Always show -->
      <i class="mdi mdi-pencil text-primary action-icon" 
         title="Edit User" 
         (click)="onEditClick($event)"></i>
      
      <!-- Change Password Icon - Always show for users -->
      <i class="mdi mdi-key-change text-warning action-icon" 
         title="Change Password" 
         (click)="onChangePasswordClick($event)"></i>
      
      <!-- Active/Inactive Toggle -->
      <!-- If user IS ACTIVE, show DEACTIVATE icon -->
      <i *ngIf="params.data.IsActive" 
         class="mdi mdi-account-remove text-danger action-icon" 
         title="Deactivate User" 
         (click)="onDeactivateClick($event)"></i>
      
      <!-- If user IS INACTIVE, show ACTIVATE icon -->
      <i *ngIf="!params.data.IsActive" 
         class="mdi mdi-account-check text-success action-icon" 
         title="Activate User" 
         (click)="onActivateClick($event)"></i>
      
      <!-- Delete Icon - Only for inactive users -->
      <i *ngIf="!params.data.IsActive" 
         class="mdi mdi-delete text-danger action-icon" 
         title="Delete User" 
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
    .text-primary:hover { color: #0056b3 !important; }
    .text-success:hover { color: #1e7e34 !important; }
    .text-warning:hover { color: #d39e00 !important; }
    .text-danger:hover { color: #bd2130 !important; }
  `]
})
export class UserActionComponent implements ICellRendererAngularComp {
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