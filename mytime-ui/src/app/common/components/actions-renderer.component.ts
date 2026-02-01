// actions-renderer.component.ts
import { Component } from '@angular/core';
import { ICellRendererAngularComp } from 'ag-grid-angular';

@Component({
  selector: 'app-actions-renderer',
  template: `
    <div class="d-flex justify-content-center gap-1">
      <a class="btn-edit" title="Edit" (click)="onEditClick($event)">
        <i class="mdi mdi-pencil"></i>
      </a>
      <a class="btn-delete" title="Delete" (click)="onDeleteClick($event)">
        <i class="mdi mdi-delete-circle"></i> </a>
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