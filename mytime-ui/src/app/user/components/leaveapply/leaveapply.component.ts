import { Component, OnInit, HostListener } from '@angular/core';
import { LeaveService } from '../../../admin/services/leave.service';
import { LeaveType } from '../../../admin/models/leave-type.model';
import { LeaveRequest } from '../../../admin/models/leave-request.model';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { LoaderService } from '../../../common/services/loader.service';
import { AccountService } from '../../../common/services/account.service';
import { AgGridModule } from 'ag-grid-angular';
import { AllCommunityModule, ColDef, GridOptions, ICellRendererParams, ModuleRegistry } from 'ag-grid-community';

ModuleRegistry.registerModules([AllCommunityModule]);

@Component({
  selector: 'app-leaveapply',
  standalone: true,
  imports: [CommonModule, FormsModule, AgGridModule],
  templateUrl: './leaveapply.component.html',
  styleUrls: ['./leaveapply.component.css']
})
export class LeaveapplyComponent implements OnInit {

  leaveTypes: LeaveType[] = [];
  leaves: LeaveRequest[] = [];

  columnDefs: ColDef[] = [];
  gridOptions!: GridOptions;

  isMobile = false;
  showForm = false;

  approvedCount = 0;
  rejectedCount = 0;
  pendingCount = 0;
  cancelledCount = 0;

  userId: number | undefined;

  leave: any = {
    LeaveTypeId: '',
    FromDate: '',
    ToDate: '',
    TotalDays: 0,
    Reason: '',
    Description: ''
  };
  errorMessage: string = '';
  successMessage: string = '';

  constructor(
    private leaveService: LeaveService,
    private loader: LoaderService,
    private accountService: AccountService
  ) { }

  ngOnInit() {

    this.checkScreen();

    this.gridOptions = {
      pagination: true,
      paginationPageSize: 20,
      animateRows: true
    };

    this.setupColumns();
    this.getLeaveTypes();
    this.loadLoggedInUserLeaves();
  }

  @HostListener('window:resize')
  checkScreen() {
    this.isMobile = window.innerWidth < 768;
    this.setupColumns();
  }

  setupColumns() {

    if (this.isMobile) {
      this.columnDefs = [
        {
          field: 'LeaveTypeId',
          headerName: 'Type',
          width: 120,
          valueGetter: (p) => this.getLeaveTypeName(p.data.LeaveTypeId),
          filter: 'agTextColumnFilter',
          sortable: true
        },
        {
          field: 'FromDate',
          headerName: 'From',
          width: 120,
          valueFormatter: (p) => new Date(p.value).toLocaleDateString(),
          filter: 'agTextColumnFilter'
        },
        {
          field: 'ToDate',
          headerName: 'To',
          width: 120,
          valueFormatter: (p) => new Date(p.value).toLocaleDateString(),
          filter: 'agTextColumnFilter',
          sortable: true
        },
        {
          field: 'Status',
          headerName: 'Status',
          width: 120,
          cellRenderer: this.statusRenderer
        },
        {
          headerName: 'Action',
          width: 120,
          cellRenderer: (params: any) => {

            const btn = document.createElement('button');
            btn.innerText = 'Cancel';
            btn.className = 'cancel-btn-grid';

            if (params.data.Status !== 'Pending') {
              btn.disabled = true;
            }

            btn.addEventListener('click', () => {
              this.cancelLeave(params.data.Id);
            });

            return btn;
          }
        }
      ];

    } else {

      this.columnDefs = [

        {
          field: 'LeaveTypeId',
          headerName: 'Leave Type',
          width: 180,
          valueGetter: (p) => this.getLeaveTypeName(p.data.LeaveTypeId),
          filter: 'agTextColumnFilter',
          sortable: true
        },

        {
          field: 'FromDate',
          headerName: 'From Date',
          width: 130,
          valueFormatter: (p) => new Date(p.value).toLocaleDateString(),
          filter: 'agTextColumnFilter',
          sortable: true
        },

        {
          field: 'ToDate',
          headerName: 'To Date',
          width: 130,
          valueFormatter: (p) => new Date(p.value).toLocaleDateString(),
          filter: 'agTextColumnFilter',
          sortable: true
        },

        {
          field: 'TotalDays',
          headerName: 'Total days',
          width: 140,
          cellClass: 'text-center',
          filter: 'agNumberColumnFilter',
          sortable: true
        },

        {
          field: 'Reason',
          headerName: 'Reason',
          width: 160,
          filter: 'agTextColumnFilter'
        },

        {
          field: 'AdminComment',
          headerName: 'Review',
          width: 160,
          filter: 'agTextColumnFilter',
          sortable: true,

          cellRenderer: (params: any) => {

            const comment = params.value;

            if (!comment || comment.trim() === '') {
              return `<span class="waiting-review">Waiting for admin response</span>`;
            }

            return `<span class="review-text">${comment}</span>`;
          },

          tooltipValueGetter: (params: any) => {
            const comment = params.value;
            return comment && comment.trim() !== ''
              ? comment
              : 'Waiting for admin response';
          }
        },

        {
          field: 'Status',
          headerName: 'Leave status',
          width: 140,
          filter: 'agTextColumnFilter',
          sortable: true,
          cellRenderer: (params: any) => {

            const status = params.value;

            let cssClass = '';

            if (status === 'Approved') cssClass = 'status-approved';
            else if (status === 'Rejected') cssClass = 'status-rejected';
            else if (status === 'Pending') cssClass = 'status-pending';
            else if (status === 'Cancelled') cssClass = 'status-cancelled';

            return `<span class="status-pill ${cssClass}">${status}</span>`;
          }
        },
        {
          headerName: 'Action',
          width: 140,
          cellRenderer: (params: any) => {

            const btn = document.createElement('button');
            btn.innerText = 'Cancel';
            btn.className = 'cancel-btn-grid';

            if (params.data.Status !== 'Pending') {
              btn.disabled = true;
            }

            btn.addEventListener('click', () => {
              this.cancelLeave(params.data.Id);
            });

            return btn;
          }
        }

      ];
    }
  }

  statusRenderer(params: any) {

    const status = params.value;

    let css = '';

    if (status === 'Approved') css = 'status-approved';
    else if (status === 'Rejected') css = 'status-rejected';
    else if (status === 'Pending') css = 'status-pending';
    else if (status === 'Cancelled') css = 'status-cancelled';

    return `<span class="status-badge ${css}">${status}</span>`;
  }

  activeRenderer(params: any) {

    return params.value
      ? `<span class="active-badge">Active</span>`
      : `<span class="inactive-badge">Inactive</span>`;
  }

  getLeaveTypes() {
    this.leaveService.GetleaveTypesAsync().subscribe(res => {
      this.leaveTypes = res;
    });
  }

  loadLoggedInUserLeaves() {

    this.loader.show();

    const user = this.accountService.getCurrentUser();
    this.userId = user?.id;

    this.leaveService.GetMyLeavesAsync(this.userId).subscribe(res => {

      this.leaves = res;

      this.calculateDashboard();

      this.loader.hide();
    });
  }

  calculateDashboard() {

    this.approvedCount = this.leaves.filter(x => x.Status === 'Approved').length;
    this.rejectedCount = this.leaves.filter(x => x.Status === 'Rejected').length;
    this.pendingCount = this.leaves.filter(x => x.Status === 'Pending').length;
    this.cancelledCount = this.leaves.filter(x => x.Status === 'Cancelled').length;

  }

  toggleForm() {
    this.showForm = true;
  }

  closeForm() {

    this.leave = {
      LeaveTypeId: null,
      FromDate: '',
      ToDate: '',
      Reason: '',
      Description: ''
    };

    this.errorMessage = '';

    this.showForm = false;   // your form visibility variable
  }
  calculateDays() {

    if (this.leave.FromDate && this.leave.ToDate) {

      const from = new Date(this.leave.FromDate);
      const to = new Date(this.leave.ToDate);

      const diff = to.getTime() - from.getTime();

      this.leave.TotalDays = diff / (1000 * 3600 * 24) + 1;

      if (this.leave.TotalDays < 0)
        this.leave.TotalDays = 0;
    }
  }

  submitLeave() {
    this.loader.show();

    if (!this.leave.LeaveTypeId || !this.leave.FromDate || !this.leave.ToDate || !this.leave.Reason) {
      this.errorMessage = "Please fill all required fields";
      this.loader.hide();
      return;
    }

    const today = new Date();
    today.setHours(0, 0, 0, 0);

    const From = new Date(this.leave.FromDate);
    const To = new Date(this.leave.ToDate);

    if (From < today || To < today) {
      this.errorMessage = "Past dates are not allowed";
      this.loader.hide();
      return;
    }

    const from = new Date(this.leave.FromDate);
    const to = new Date(this.leave.ToDate);

    const totalDays = (to.getTime() - from.getTime()) / (1000 * 3600 * 24) + 1;

    if (totalDays <= 0) {
      this.errorMessage = "Invalid date range";
      this.loader.hide();
      return;
    }

    const payload = {
      userId: this.userId,
      leaveTypeId: +this.leave.LeaveTypeId,
      fromDate: this.leave.FromDate,
      toDate: this.leave.ToDate,
      totalDays: totalDays,
      reason: this.leave.Reason,
      description: this.leave.Description || ""
    };

    this.leaveService.ApplyleaveAsync(payload).subscribe({
      next: () => {

        this.showToast("Leave Applied Successfully", "success");
        this.refreshForm();

        this.closeForm();
        this.loadLoggedInUserLeaves();

        this.loader.hide();
      },
      error: err => {
        this.errorMessage = err?.error?.detail || "Something went wrong";
        this.loader.hide();
      }
    });
  }

  refreshForm() {
    this.leave = {
      LeaveTypeId: null,
      FromDate: '',
      ToDate: '',
      Reason: '',
      Description: ''
    };

    this.errorMessage = '';
  }

  showToast(message: string, type: 'success' | 'error') {

    const toast = document.createElement('div');
    toast.className = `custom-toast ${type}`;

    toast.innerHTML = `
    <div class="toast-content">
      <span>${message}</span>
      <button class="close-btn">✖</button>
    </div>
    <div class="progress-bar"></div>
  `;

    document.body.appendChild(toast);

    toast.querySelector('.close-btn')?.addEventListener('click', () => {
      toast.remove();
    });
  }
  cancelLeave(id: number) {

    const reason = prompt("Cancel reason");
    if (!reason) return;
    this.leaveService.CancelLeaveAsync(id, { cancelReason: reason })
      .subscribe(() => {
        this.loadLoggedInUserLeaves();
      });
  }

  getLeaveTypeName(id: number) {
    const type = this.leaveTypes.find(x => x.Id === id);
    return type ? type.Name : '';
  }
}