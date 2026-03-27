// attendance-actions-renderer.component.ts
import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { ICellRendererAngularComp } from 'ag-grid-angular';

@Component({
  selector: 'app-attendance-actions-renderer',
  imports: [CommonModule],
  standalone: true,
  template: `
    <div class="d-flex justify-content-center gap-2">
      <!-- Edit Button - ONLY show if no CheckOutTime -->
      <i *ngIf="!hasCheckOutTime" 
         class="mdi mdi-pencil text-primary attendance-action-icon" 
         title="Edit Attendance" 
         (click)="onEditClick($event)"></i>
      
      <!-- Delete Button - Always show -->
      <i class="mdi mdi-delete-circle text-danger attendance-action-icon" 
         title="Delete Attendance" 
         (click)="onDeleteClick($event)"></i>
    </div>
  `,
  styles: [`
    .attendance-action-icon {
      cursor: pointer;
      font-size: 22px;
      padding: 6px;
      border-radius: 6px;
      transition: all 0.2s ease;
    }
    
    .attendance-action-icon:hover {
      transform: scale(1.1);
      background-color: rgba(0, 0, 0, 0.05);
    }
    
    /* For touch devices */
    .attendance-action-icon:active {
      transform: scale(0.95);
      background-color: rgba(0, 0, 0, 0.1);
    }
    
    .text-primary:hover { color: #0056b3 !important; }
    .text-danger:hover { color: #bd2130 !important; }
    
    /* Larger touch targets for mobile */
    @media (max-width: 768px) {
      .attendance-action-icon {
        padding: 8px;
        font-size: 24px;
      }
    }
  `]
})
export class AttendanceActionsRendererComponent implements ICellRendererAngularComp {
  params: any;

  // Check if CheckOutTime exists (not null, undefined, or empty string)
  get hasCheckOutTime(): boolean {
    const checkOutTime = this.params?.data?.CheckOutTime;
    // Return true if CheckOutTime exists and is not empty
    return checkOutTime !== null && checkOutTime !== undefined && checkOutTime !== '';
  }

  agInit(params: any): void {
    this.params = params;
  }

  refresh(params: any): boolean {
    this.params = params;
    return true;
  }

  onEditClick(event: MouseEvent): void {
    event.stopPropagation();
    if (this.params.onEditClick) {
      this.params.onEditClick(this.params.data);
    }
  }

  onDeleteClick(event: MouseEvent): void {
    event.stopPropagation();
    if (this.params.onDeleteClick) {
      this.params.onDeleteClick(this.params.data);
    }
  }
}