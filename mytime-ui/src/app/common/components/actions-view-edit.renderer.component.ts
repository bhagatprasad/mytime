import { Component } from '@angular/core';
import { ICellRendererAngularComp } from 'ag-grid-angular';

@Component({
  selector: 'app-actions-view-edit.renderer',
  template: `
    <div class="d-flex justify-content-center gap-1">
      <!-- Edit -->
      <a class="btn-edit" title="Edit" (click)="onEditClick($event)">
        <i class="mdi mdi-pencil"></i>
      </a>
      <!-- View -->
      <a class="btn-view" title="View" (click)="onViewClick($event)">
        <i class="mdi mdi-eye"></i>
      </a>
     </div>` ,
     styleUrls: ['./actions-view-edit.renderer.component.css']
})

export class UseractionsViewEdit implements ICellRendererAngularComp {
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
    onViewClick(event: MouseEvent): void {
        event.stopPropagation();
        if (this.params.onViewClick) {
            this.params.onViewClick(this.params.data);
        }
    }
}
