import { Component } from '@angular/core';
import { ICellRendererAngularComp } from 'ag-grid-angular';

@Component({
  selector: 'app-mobile-actions-renderer',
  template: `
    <div class="d-flex justify-content-center gap-1 mobile-actions-wrapper">

      <!-- Download Button -->
      <a 
        class="d-flex align-items-center mobile-action-btn download-btn"
        (click)="onDownloadClick($event)"
        title="Download"
      >
        <i class="mdi mdi-download"></i>
        <span class="btn-text">Download</span>
      </a>

      <!-- Edit Button -->
      <a 
        class="d-flex align-items-center mobile-action-btn edit-btn"
        (click)="onEditClick($event)"
        title="Edit"
      >
        <i class="mdi mdi-pencil"></i>
        <span class="btn-text">Edit</span>
      </a>

      <!-- Delete Button -->
      <a 
        class="d-flex align-items-center mobile-action-btn delete-btn"
        (click)="onDeleteClick($event)"
        title="Delete"
      >
        <i class="mdi mdi-delete"></i>
        <span class="btn-text">Delete</span>
      </a>

    </div>
  `,
  styles: [`
    .mobile-actions-wrapper {
      padding: 2px;
      height: 100%;
      display: flex;
      align-items: center;
      flex-wrap: wrap;
    }

    .mobile-action-btn {
      padding: 2px 6px;
      font-size: 11px;
      line-height: 1.2;
      border-radius: 3px;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      white-space: nowrap;
      transition: all 0.15s ease-in-out;
      text-decoration: none;
      gap: 2px;
      min-height: 20px;
    }

    /* Download */
    .download-btn {
      background-color: #198754;
      border: 1px solid #198754;
      color: white;
    }

    .download-btn:hover {
      background-color: #157347;
      border-color: #146c43;
      color: white;
    }

    .download-btn:active {
      background-color: #146c43;
      border-color: #13653f;
    }

    /* Edit */
    .edit-btn {
      background-color: #0d6efd;
      border: 1px solid #0d6efd;
      color: white;
    }

    .edit-btn:hover {
      background-color: #0b5ed7;
      border-color: #0a58ca;
      color: white;
    }

    /* Delete */
    .delete-btn {
      background-color: #dc3545;
      border: 1px solid #dc3545;
      color: white;
    }

    .delete-btn:hover {
      background-color: #bb2d3b;
      border-color: #b02a37;
      color: white;
    }

    .mobile-action-btn i {
      font-size: 12px;
      line-height: 1;
    }

    /* Mobile-specific */
    @media (max-width: 768px) {
      .mobile-action-btn {
        padding: 3px 8px;
        min-height: 24px;
        font-size: 12px;
      }

      .mobile-action-btn i {
        font-size: 13px;
      }
    }

    /* Very small screens: icon only */
    @media (max-width: 480px) {
      .btn-text {
        display: none;
      }

      .mobile-action-btn {
        padding: 3px;
        min-width: 24px;
        min-height: 24px;
        justify-content: center;
        border-radius: 20px;
      }

      .mobile-action-btn i {
        margin-right: 0;
        font-size: 14px;
      }

      .mobile-actions-wrapper {
        gap: 2px;
      }
    }

    @media print {
      .mobile-action-btn {
        display: none;
      }
    }
  `]
})
export class MobileActionsRendererComponent implements ICellRendererAngularComp {

  params: any;

  agInit(params: any): void {
    this.params = params;
  }

  refresh(): boolean {
    return false;
  }

  onDownloadClick(event: MouseEvent): void {
    event.stopPropagation();
    if (this.params.onDownloadClick) {
      this.params.onDownloadClick(this.params.data);
    }
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
