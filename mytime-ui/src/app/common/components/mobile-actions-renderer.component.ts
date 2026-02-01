import { Component } from '@angular/core';
import { ICellRendererAngularComp } from 'ag-grid-angular';

@Component({
  selector: 'app-mobile-actions-renderer',
  template: `
    <div class="d-flex justify-content-center mobile-actions-wrapper">
      <a 
        class="d-flex align-items-center"
        (click)="onEdit()"
        [attr.title]="'Edit ' + (params?.data?.name || params?.data?.title || 'item')"
      >
        <i class="mdi mdi-pencil me-1"></i>
      </a>
    </div>
  `,
  styles: [`
    .mobile-actions-wrapper {
      padding: 2px;
      height: 100%;
      display: flex;
      align-items: center;
    }
    
    .mobile-edit-btn {
      padding: 0.25rem 0.5rem;
      font-size: 0.875rem;
      line-height: 1.5;
      border-radius: 0.2rem;
      background-color: #0d6efd;
      border-color: #0d6efd;
      color: white;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      white-space: nowrap;
      transition: color 0.15s ease-in-out, background-color 0.15s ease-in-out, 
                  border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
    }
    
    .mobile-edit-btn:hover {
      background-color: #0b5ed7;
      border-color: #0a58ca;
      color: white;
    }
    
    .mobile-edit-btn:active {
      background-color: #0a58ca;
      border-color: #0a53be;
    }
    
    .mobile-edit-btn i {
      font-size: 16px;
      line-height: 1;
    }
    
    /* Mobile-specific optimizations */
    @media (max-width: 768px) {
      .mobile-edit-btn {
        padding: 0.5rem 1rem;
        min-height: 20px;
        font-size: 14px;
      }
      
      .mobile-edit-btn i {
        font-size: 18px;
        margin-right: 6px;
      }
    }
    
    /* For very small screens, make it icon-only */
    @media (max-width: 480px) {
      .mobile-edit-btn span {
        display: none;
      }
      
      .mobile-edit-btn i {
        margin-right: 0;
      }
      
      .mobile-edit-btn {
        padding: 0.5rem;
        min-width: 20px;
        min-height: 20px;
        justify-content: center;
      }
    }
  `]
})
export class MobileActionsRendererComponent implements ICellRendererAngularComp {
  params: any;

  agInit(params: any): void {
    this.params = params;
  }

  refresh(params: any): boolean {
    return false;
  }

  onEdit(): void {
    if (this.params && this.params.onEditClick) {
      this.params.onEditClick(this.params.data);
    }
  }
}