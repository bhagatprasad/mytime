// actions-renderer.component.ts
import { Component } from '@angular/core';
import { ICellRendererAngularComp } from 'ag-grid-angular';

@Component({
    selector: 'app-salary-action',
    template: `
    <div class="d-flex justify-content-center gap-1">
    <!-- View -->
      <a class="btn-download" title="Download" (click)="onDownloadClick($event)">
        <i class="mdi mdi-download"></i>
      </a>
      <!-- Delete -->
      <a class="btn-download" title="View" (click)="onViewClick($event)">
        <i class="mdi mdi-eye-circle"></i>
      </a>
    </div>
  `,
    styleUrls: ['./user-action-component.css']
})
export class UserActionComponent implements ICellRendererAngularComp {
    private params: any;

    agInit(params: any): void {
        this.params = params;
    }

    refresh(params: any): boolean {
        this.params = params;
        return true;
    }
    onDownloadClick(event: MouseEvent): void {
        event.stopPropagation();
        if (this.params.onDownloadClick) {
            this.params.onDownloadClick(this.params.data);
        }
    }
    onViewClick(event: MouseEvent): void {
        event.stopPropagation();
        if (this.params.onViewClick) {
            this.params.onViewClick(this.params.data);
        }
    }
}
