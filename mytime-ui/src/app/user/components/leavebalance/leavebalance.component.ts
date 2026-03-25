import { Component, OnInit } from '@angular/core';
import { leavebalanceservice } from '../../../admin/services/leavebalance.service';
import { LeaveTypeService } from '../../../admin/services/leavetype.service';
import { LeaveType } from '../../../admin/models/leave-type.model';
import { LeaveBalance } from '../../../admin/models/leavebalance';
import { LoaderService } from '../../../common/services/loader.service';
import { AccountService } from '../../../common/services/account.service';
import { LeaveService } from '../../../admin/services/leave.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-leavebalance',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './leavebalance.component.html',
  styleUrl: './leavebalance.component.css'
})
export class LeavebalanceComponent implements OnInit {

  constructor(private leaveBalanceService: leavebalanceservice, private accountService: AccountService, private loader: LoaderService, private leaveService: LeaveService) { }

  leaveTypes: LeaveType[] = [];
  leavebalance: LeaveBalance[] = [];
  userId: number | undefined;

  ngOnInit() {
    this.getLeaveTypes();
    this.loadLoggedInUserLeavesBalance();
  }

  loadLoggedInUserLeavesBalance(): void {
    this.loader.show();
    const user = this.accountService.getCurrentUser();
    this.userId = user?.id;
    if (!user?.id) {
      console.warn('No logged-in user found');
      this.loader.hide();
      return;

    }

    this.leaveBalanceService.getleavebalancebyuserAsync(user.id).subscribe({
      next: (res: any) => {
        this.leavebalance = res;
        this.loader.hide();
      },
      error: (err) => {
        console.error('Error fetching leaves', err);
        this.loader.hide();
      }
    });
  }

  getLeaveTypes() {
    this.leaveService.GetleaveTypesAsync()
      .subscribe(res => {
        this.leaveTypes = res;
      });
  }

  getLeaveTypeName(id: number): string {
    const type = this.leaveTypes.find((t: any) => t.Id === id);
    return type ? type.Name : 'Unknown';
  }

  getAllLeaveCards() {

    return this.leaveTypes.map(type => {

      const balance = this.leavebalance.find(
        b => b.LeaveTypeId === type.Id
      );

      return {
        LeaveTypeId: type.Id,
        Name: type.Name,
        TotalLeaves: balance ? balance.TotalLeaves : type.MaxDaysPerYear,
        UsedLeaves: balance ? balance.UsedLeaves : 0,
        RemainingLeaves: balance ? balance.RemainingLeaves : type.MaxDaysPerYear
      };
    });
  }

  getCircleColor(leave: any): string {

  const percent = (leave.UsedLeaves / leave.TotalLeaves) * 100;

  if (percent < 40) {
    return '#6fcf97'; // soft green
  }

  if (percent < 75) {
    return '#f2c94c'; // soft yellow
  }

  return '#eb5757'; // soft red
}
}
