// actions-renderer.component.ts
import { Component } from '@angular/core';
import { ICellRendererAngularComp } from 'ag-grid-angular';

@Component({
  selector: 'app-actions-renderer',
  template: `
    <div class="d-flex justify-content-center gap-1">
      <button class="btn btn-sm btn-outline-primary" title="Edit" (click)="onEditClick($event)">
        <i class="mdi mdi-pencil"></i>
      </button>
      <button class="btn btn-sm btn-outline-danger" title="Delete" (click)="onDeleteClick($event)">
        <i class="mdi mdi-delete"></i>
      </button>
    </div>
  `
})
export class ActionsRendererComponent implements ICellRendererAngularComp {
  private params: any;

  agInit(params: any): void {
    this.params = params;
  }

  refresh(params: any): boolean {
    return false;
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