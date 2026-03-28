import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { ICellRendererAngularComp } from 'ag-grid-angular';

@Component({
    selector: 'app-attendence-actions-renderer',
    standalone: true,
    template: `
    <div class="d-flex justify-content-center gap-1">
      <!-- Edit - only show if no CheckOutTime -->
      <a *ngIf="!hasCheckOutTime" class="btn-edit" title="Edit" (click)="onEditClick($event)">
        <i class="mdi mdi-pencil"></i>
      </a>

      <!-- Delete - always show -->
      <a class="btn-delete" title="Delete" (click)="onDeleteClick($event)">
        <i class="mdi mdi-delete-circle"></i>
      </a>
    </div>
  `,
    imports: [CommonModule],
    styleUrls: ['./attendence-action-componen.css']
})
export class AttendancectionsRendererComponent implements ICellRendererAngularComp {
    private params: any;

    // Check if CheckOutTime is missing (null, undefined, or empty string)
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