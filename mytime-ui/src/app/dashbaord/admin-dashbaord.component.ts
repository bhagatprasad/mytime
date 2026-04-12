// admin-dashboard.component.ts
import { Component, OnInit, AfterViewInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { LoaderService } from '../common/services/loader.service';
import { NotifyService } from '../common/services/notify.service';

@Component({
  selector: 'app-admin-dashboard',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './admin-dashbaord.component.html',
  styleUrls: ['./admin-dashbaord.component.css']
})
export class AdminDashbaordComponent implements OnInit, AfterViewInit {

  // Statistics Data
  totalEmployees: number = 284;
  totalEmployeesGrowth: number = 12;
  presentToday: number = 256;
  attendanceRate: number = 90;
  onLeave: number = 18;

  // Payroll Data
  totalPayslips: number = 284;
  totalPayslipsGrowth: number = 8;
  totalSalaryDisbursed: number = 2845000;
  salaryGrowth: number = 15;
  pendingPayments: number = 12;
  thisMonthSalary: number = 2850000;

  // Leave Data
  pendingLeaves: number = 24;
  approvedLeaves: number = 156;
  totalLeaves: number = 342;
  leaveRequests: number = 18;

  // Timesheet Data
  pendingTimesheets: number = 32;
  submittedTimesheets: number = 252;
  totalTimesheets: number = 284;
  timesheetCompletion: number = 88;

  // Help Desk Data
  openTickets: number = 15;
  resolvedTickets: number = 128;
  totalTickets: number = 143;
  ticketResolutionRate: number = 89;

  // Quick Stats for Cards
  quickStats = [
    { title: 'Total Employees', value: '284', icon: 'people-fill', color: '#3b82f6', change: '+12', changeType: 'increase', route: 'employees' },
    { title: 'Present Today', value: '256', icon: 'calendar-check-fill', color: '#10b981', change: '90%', changeType: 'attendance', route: 'attendance' },
    { title: 'On Leave', value: '18', icon: 'umbrella-fill', color: '#f59e0b', change: '6%', changeType: 'leave', route: 'leave-management' },
    { title: 'Pending Leaves', value: '24', icon: 'hourglass-split', color: '#ef4444', change: '+8', changeType: 'pending', route: 'leave-management' }
  ];

  // Recent Activities
  recentActivities = [
    { user: 'John Doe', action: 'Submitted timesheet', time: '2 hours ago', type: 'timesheet' },
    { user: 'Sarah Smith', action: 'Requested leave', time: '3 hours ago', type: 'leave' },
    { user: 'Mike Johnson', action: 'Generated payslip', time: '5 hours ago', type: 'payslip' },
    { user: 'Emma Wilson', action: 'Updated documents', time: '1 day ago', type: 'document' },
    { user: 'Robert Brown', action: 'Raised help desk ticket', time: '1 day ago', type: 'helpdesk' }
  ];

  // Upcoming Events
  upcomingEvents = [
    { title: 'Payroll Processing', date: 'Mar 31, 2025', type: 'payroll', priority: 'high' },
    { title: 'Holiday - Good Friday', date: 'Apr 18, 2025', type: 'holiday', priority: 'medium' },
    { title: 'Performance Reviews Due', date: 'Apr 15, 2025', type: 'review', priority: 'high' },
    { title: 'Tax Declaration Deadline', date: 'Mar 31, 2025', type: 'tax', priority: 'urgent' }
  ];

  // Department Distribution
  departments = [
    { name: 'Engineering', count: 98, percentage: 35, color: '#3b82f6' },
    { name: 'Sales', count: 52, percentage: 18, color: '#10b981' },
    { name: 'Marketing', count: 38, percentage: 13, color: '#f59e0b' },
    { name: 'HR', count: 24, percentage: 8, color: '#ef4444' },
    { name: 'Finance', count: 22, percentage: 8, color: '#8b5cf6' },
    { name: 'Operations', count: 30, percentage: 11, color: '#06b6d4' },
    { name: 'Others', count: 20, percentage: 7, color: '#6b7280' }
  ];

  // Module Cards Configuration
  moduleCards = [
    { title: 'Payslips', icon: 'receipt', description: 'Manage employee payslips', count: '284', color: '#3b82f6', route: 'payslips', action: 'View All' },
    { title: 'Salaries', icon: 'currency-rupee', description: 'Salary processing & history', count: '₹28.45L', color: '#10b981', route: 'salaries', action: 'Process' },
    { title: 'Employee Management', icon: 'people', description: 'Employee profiles & records', count: '284', color: '#f59e0b', route: 'employees', action: 'Manage' },
    { title: 'Document Management', icon: 'folder-check', description: 'HR documents & policies', count: '156', color: '#ef4444', route: 'documents', action: 'View' },
    { title: 'Holiday Management', icon: 'calendar-heart', description: 'Company holidays', count: '12', color: '#8b5cf6', route: 'holidays', action: 'Manage' },
    { title: 'Leave Management', icon: 'umbrella', description: 'Leave requests & approvals', count: '24', color: '#ec489a', route: 'leave-management', action: 'Approve' },
    { title: 'Timesheet Management', icon: 'clock-history', description: 'Timesheet submissions', count: '32', color: '#06b6d4', route: 'timesheets', action: 'Review' },
    { title: 'Help Desk', icon: 'headset', description: 'Support tickets', count: '15', color: '#6b7280', route: 'helpdesk', action: 'Respond' }
  ];

  // Recent Payslips
  recentPayslips = [
    { employee: 'John Doe', month: 'March 2025', amount: '₹52,450', status: 'Generated' },
    { employee: 'Sarah Smith', month: 'March 2025', amount: '₹48,200', status: 'Generated' },
    { employee: 'Mike Johnson', month: 'March 2025', amount: '₹61,750', status: 'Processing' },
    { employee: 'Emma Wilson', month: 'February 2025', amount: '₹45,800', status: 'Disbursed' }
  ];

  // Pending Leave Requests
  pendingLeaveRequests = [
    { employee: 'Alice Cooper', type: 'Sick Leave', days: 2, date: 'Mar 25-26, 2025' },
    { employee: 'Bob Martin', type: 'Annual Leave', days: 5, date: 'Apr 1-5, 2025' },
    { employee: 'Carol Davis', type: 'Personal Leave', days: 1, date: 'Mar 28, 2025' }
  ];

  // Timesheet Summary
  timesheetSummary = [
    { department: 'Engineering', submitted: 42, pending: 8, total: 50 },
    { department: 'Sales', submitted: 28, pending: 4, total: 32 },
    { department: 'Marketing', submitted: 22, pending: 3, total: 25 },
    { department: 'Others', submitted: 38, pending: 5, total: 43 }
  ];

  // Help Desk Tickets
  helpDeskTickets = [
    { id: 'TKT-001', subject: 'Salary slip not visible', priority: 'High', status: 'Open', assignedTo: 'Support Team' },
    { id: 'TKT-002', subject: 'Leave balance incorrect', priority: 'Medium', status: 'In Progress', assignedTo: 'HR Team' },
    { id: 'TKT-003', subject: 'Timesheet submission issue', priority: 'Low', status: 'Open', assignedTo: 'IT Support' }
  ];

  constructor(
    private loader: LoaderService,
    private notify: NotifyService
  ) { }

  ngOnInit(): void {
    this.loadDashboardData();
  }

  ngAfterViewInit(): void {
    this.initCharts();
  }

  loadDashboardData(): void {
    this.loader.show();
    // Simulate API call
    setTimeout(() => {
      this.loader.hide();
      this.notify.showSuccess('Dashboard data loaded successfully!');
    }, 1000);
  }

  initCharts(): void {
    // Initialize charts here
    this.initDepartmentChart();
    this.initAttendanceChart();
    this.initPayrollChart();
  }

  initDepartmentChart(): void {
    // Department distribution chart would be initialized here
    console.log('Department chart initialized');
  }

  initAttendanceChart(): void {
    // Attendance chart would be initialized here
    console.log('Attendance chart initialized');
  }

  initPayrollChart(): void {
    // Payroll trend chart would be initialized here
    console.log('Payroll chart initialized');
  }

  navigateTo(route: string): void {
    console.log(`Navigating to: ${route}`);
    // this.router.navigate([`/admin/${route}`]);
    this.notify.showInfo(`Navigating to ${route} module`);
  }

  getStatusClass(status: string): string {
    switch (status.toLowerCase()) {
      case 'generated': return 'status-generated';
      case 'processing': return 'status-processing';
      case 'disbursed': return 'status-disbursed';
      case 'open': return 'status-open';
      case 'in progress': return 'status-progress';
      default: return '';
    }
  }

  getPriorityClass(priority: string): string {
    switch (priority.toLowerCase()) {
      case 'urgent': return 'priority-urgent';
      case 'high': return 'priority-high';
      case 'medium': return 'priority-medium';
      case 'low': return 'priority-low';
      default: return '';
    }
  }
  /* Helper Function in Component */
getActivityIcon(type: string): string {
    const icons: { [key: string]: string } = {
      timesheet: 'clock-history',
      leave: 'umbrella',
      payslip: 'receipt',
      document: 'file-text',
      helpdesk: 'headset'
    };
    return icons[type] || 'bell';
  }
}