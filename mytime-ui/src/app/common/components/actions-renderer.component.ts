// actions-renderer.component.ts
import { Component } from '@angular/core';
import { ICellRendererAngularComp } from 'ag-grid-angular';

@Component({
  selector: 'app-actions-renderer',
  template: `
    <div class="d-flex justify-content-center gap-1">
      <button class="btn btn-sm btn-info btn-edit" title="Edit" (click)="onEditClick($event)">
        <i class="icon-cog"></i> Edit
      </button>
      <button class="btn btn-sm btn-danger btn-delete" title="Delete" (click)="onDeleteClick($event)">
        <i class="icon-disc"></i> Delete
      </button>
    </div>
  `,
  styleUrls: [
    './actions-renderer.component.css'
  ]
})
export class ActionsRendererComponent implements ICellRendererAngularComp {
  private params: any;

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