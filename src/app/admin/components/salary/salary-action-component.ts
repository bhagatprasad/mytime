// actions-renderer.component.ts
import { Component } from '@angular/core';
import { ICellRendererAngularComp } from 'ag-grid-angular';

@Component({
    selector: 'app-salary-action',
    template: `
    <div class="d-flex justify-content-center gap-1">
      <!-- Edit -->
      <a class="btn-edit" title="Edit" (click)="onEditClick($event)">
        <i class="mdi mdi-pencil"></i>
      </a>

      <!-- Delete -->
      <a class="btn-delete" title="Delete" (click)="onDeleteClick($event)">
        <i class="mdi mdi-delete-circle"></i>
      </a>
      <!-- Delete -->
      <a class="btn-download" title="Download" (click)="onDownloadClick($event)">
        <i class="mdi mdi-download"></i>
      </a>
    </div>
  `,
    styleUrls: ['./salary-action-component.css']
})
export class SalaryActionComponent implements ICellRendererAngularComp {
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

    onDownloadClick(event: MouseEvent): void {
        event.stopPropagation();
        if (this.params.onDownloadClick) {
            this.params.onDownloadClick(this.params.data);
        }
    }
    onDeleteClick(event: MouseEvent): void {
        event.stopPropagation();
        if (this.params.onDeleteClick) {
            this.params.onDeleteClick(this.params.data);
        }
    }
}
