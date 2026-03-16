import { Component, OnInit } from '@angular/core';
import { LeaveService } from '../../../admin/services/leave.service';
import { LeaveType } from '../../../admin/models/leave-type.model';
import { LeaveRequest } from '../../../admin/models/leave-request.model';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AuditFieldsService } from '../../../common/services/auditfields.service';
import { LoaderService } from '../../../common/services/loader.service';
import { AccountService } from '../../../common/services/account.service';
import { ToastrService } from 'ngx-toastr';

@Component({
  selector: 'app-leaveapply',
  imports: [CommonModule, FormsModule],
  templateUrl: './leaveapply.component.html',
  styleUrls: ['./leaveapply.component.css'],
  standalone: true

})
export class LeaveapplyComponent implements OnInit {

  leaveTypes: LeaveType[] = [];
  leaves: LeaveRequest[] = [];

  showForm = false;
  selectedFile: any;

  // userId = 20;

  approvedCount = 0;
  rejectedCount = 0;
  pendingCount = 0;
  cancelledCount = 0;

  leave: {
    LeaveTypeId?: number | null;
    FromDate?: string | Date;
    ToDate?: string | Date;
    TotalDays?: number;
    Reason?: string;
    Description?: string;
  } = {
      LeaveTypeId: null,
      FromDate: '',
      ToDate: '',
      TotalDays: 0,
      Reason: '',
      Description: ''
    };
  userId: number | undefined;
  snackBar: any;

  constructor(private leaveService: LeaveService,
    private auditservice: AuditFieldsService,
    private loader: LoaderService,
    private accountService: AccountService,
    private toastr: ToastrService) { }

  ngOnInit() {
    this.getLeaveTypes();
    this.loadLoggedInUserLeaves();
  }

  toggleForm() {
    this.showForm = true;
  }

  closeForm() {
    this.showForm = false;
    this.resetForm();
  }

  getLeaveTypes() {
    this.leaveService.GetleaveTypesAsync()
      .subscribe(res => {
        this.leaveTypes = res;
      });
  }

  loadLoggedInUserLeaves(): void {
    this.loader.show();
    const user = this.accountService.getCurrentUser();
    this.userId = user?.id;
    if (!user?.id) {
      console.warn('No logged-in user found');
      this.loader.hide();
      return;

    }

    this.leaveService.GetMyLeavesAsync(user.id).subscribe({
      next: (res: any) => {
        this.leaves = res;
        this.calculateDashboard();
        this.loader.hide();
      },
      error: (err) => {
        console.error('Error fetching leaves', err);
        this.loader.hide();
      }
    });
  }

  calculateDashboard() {

    this.approvedCount = this.leaves.filter(x => x.Status === 'Approved').length;
    this.rejectedCount = this.leaves.filter(x => x.Status === 'Rejected').length;
    this.pendingCount = this.leaves.filter(x => x.Status === 'Pending').length;
    this.cancelledCount = this.leaves.filter(x => x.Status === 'Cancelled').length;

  }

  calculateDays() {
    if (this.leave.FromDate && this.leave.ToDate) {
      const from = new Date(this.leave.FromDate);
      const to = new Date(this.leave.ToDate);
      const diff = to.getTime() - from.getTime();
      this.leave.TotalDays = diff / (1000 * 3600 * 24) + 1;
      if (this.leave.TotalDays < 0) this.leave.TotalDays = 0;
    }
  }

  onFileSelected(event: any) {

    if (event.target.files.length > 0) {
      this.selectedFile = event.target.files[0];
    }

  }

  submitLeave() {
    this.loader.show();

    if (!this.leave.LeaveTypeId || !this.leave.FromDate || !this.leave.ToDate || !this.leave.Reason) {
      alert("Please fill all required fields");
      return;
    }

    // Calculate totalDays
    const from = new Date(this.leave.FromDate);
    const to = new Date(this.leave.ToDate);
    const totalDays = (to.getTime() - from.getTime()) / (1000 * 3600 * 24) + 1;

    if (totalDays <= 0) {
      alert("Invalid date range");
      return;
    }

    // Prepare API payload with lowercase keys as backend expects
    const payload = {
      userId: this.userId,
      leaveTypeId: +this.leave.LeaveTypeId, // string -> number
      fromDate: this.leave.FromDate,        // string OK
      toDate: this.leave.ToDate,            // string OK
      totalDays: totalDays,
      reason: this.leave.Reason,
      description: this.leave.Description || ""
    };

    this.leaveService.ApplyleaveAsync(payload).subscribe({
      next: () => {
        // alert("Leave Applied Successfully");
        this.closeForm();
        this.loadLoggedInUserLeaves();
        this.loader.hide();// refresh grid
      },
      error: err => {
        console.error("Error applying leave", err);
        alert("Error applying leave: " + (err.error?.message || "Check your data"));
      }
    });
  }

  cancelLeave(id: number) {

    const reason = prompt("Enter cancel reason");

    if (!reason) return;

    this.leaveService.CancelLeaveAsync(id, { cancelReason: reason })
      .subscribe(() => {

        alert("Leave Cancelled");

        this.loadLoggedInUserLeaves();

      });
  }

  getLeaveTypeName(id: number) {

    const type = this.leaveTypes.find(x => x.Id === id);

    return type ? type.Name : '';

  }

  resetForm() {
    this.leave = {
      LeaveTypeId: null,
      FromDate: '',
      ToDate: '',
      TotalDays: 0,
      Reason: '',
      Description: ''
    };
  }

}