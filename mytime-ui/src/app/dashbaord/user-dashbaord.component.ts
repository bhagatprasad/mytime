// user-dashboard.component.ts
import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-user-dashboard',
  standalone: true,
  imports: [CommonModule,RouterModule],
  templateUrl: './user-dashbaord.component.html',
  styleUrls: ['./user-dashbaord.component.css']
})
export class UserDashboardComponent implements OnInit {
  
  // Current date, time, location, shift
  currentDate: string = '';
  currentTime: string = '';
  currentDay: string = '';
  currentLocation: string = 'Hi-Tech City, Hyderabad';
  shiftTiming: string = '09:00 AM - 06:00 PM';
  shiftType: string = 'General Shift';
  
  // Upcoming Holidays
  upcomingHolidays = [
    { name: 'Ugadi', date: 'Mar 30, 2025', day: 'Sunday' },
    { name: 'Ramzan Eid', date: 'Mar 31, 2025', day: 'Monday' },
    { name: 'Ambedkar Jayanti', date: 'Apr 14, 2025', day: 'Monday' },
    { name: 'Mahavir Jayanti', date: 'Apr 17, 2025', day: 'Thursday' },
    { name: 'Good Friday', date: 'Apr 18, 2025', day: 'Friday' }
  ];
  
  // Payslips Data
  payslips = [
    { month: 'March 2025', amount: '₹52,450', downloadUrl: '#' },
    { month: 'February 2025', amount: '₹52,450', downloadUrl: '#' },
    { month: 'January 2025', amount: '₹51,890', downloadUrl: '#' },
    { month: 'December 2024', amount: '₹51,200', downloadUrl: '#' }
  ];
  
  // IT Declarations
  declarations = [
    { name: 'House Rent Allowance (HRA)', status: 'Pending', statusClass: 'pending', deadline: 'Mar 31, 2025' },
    { name: 'Medical Insurance', status: 'Approved', statusClass: 'approved', deadline: 'Dec 31, 2024' },
    { name: 'Leave Travel Allowance (LTA)', status: 'Not Filed', statusClass: 'pending', deadline: 'Mar 31, 2025' },
    { name: 'Section 80C Investments', status: 'Under Review', statusClass: 'review', deadline: 'Mar 31, 2025' },
    { name: 'NPS Contribution', status: 'Approved', statusClass: 'approved', deadline: 'Feb 15, 2025' }
  ];
  
  // POI / Documents
  poiDocuments = [
    { name: 'Aadhaar Card', status: 'Verified', statusClass: 'verified', icon: 'check-circle-fill' },
    { name: 'PAN Card', status: 'Verified', statusClass: 'verified', icon: 'check-circle-fill' },
    { name: 'Passport', status: 'Pending', statusClass: 'pending', icon: 'clock-history' },
    { name: 'Voter ID', status: 'Not Submitted', statusClass: 'not-submitted', icon: 'exclamation-circle-fill' },
    { name: 'Bank Account', status: 'Verified', statusClass: 'verified', icon: 'check-circle-fill' },
    { name: 'Driving License', status: 'Expiring Soon', statusClass: 'warning', icon: 'exclamation-triangle-fill' }
  ];
  
  // Quick Access Items
  quickAccessItems = [
    { name: 'Attendance', icon: 'calendar-check', route: 'attendance', color: '#3b82f6' },
    { name: 'Leave', icon: 'umbrella', route: 'leave', color: '#10b981' },
    { name: 'Expense', icon: 'wallet2', route: 'expense', color: '#f59e0b' },
    { name: 'Calendar', icon: 'calendar-week', route: 'calendar', color: '#8b5cf6' },
    { name: 'Helpdesk', icon: 'headset', route: 'helpdesk', color: '#ef4444' },
    { name: 'Learning', icon: 'mortarboard', route: 'learning', color: '#06b6d4' },
    { name: 'Team', icon: 'people', route: 'team', color: '#ec489a' },
    { name: 'Assets', icon: 'laptop', route: 'assets', color: '#6b7280' }
  ];
  
  // Track Requests
  trackRequests = [
    { id: 'REQ-1001', item: 'Laptop Replacement', status: 'In Transit', statusClass: 'in-transit', date: 'Mar 20, 2025' },
    { id: 'REQ-1002', item: 'Cab Facility', status: 'Approved', statusClass: 'approved', date: 'Mar 22, 2025' },
    { id: 'REQ-1003', item: 'Monitor Request', status: 'Pending', statusClass: 'pending', date: 'Mar 23, 2025' },
    { id: 'REQ-1004', item: 'Leave Application', status: 'Approved', statusClass: 'approved', date: 'Mar 18, 2025' },
    { id: 'REQ-1005', item: 'Software Access', status: 'In Progress', statusClass: 'in-progress', date: 'Mar 21, 2025' }
  ];
  
  // Review Data
  reviewData = {
    rating: 4.5,
    maxRating: 5,
    percentage: 90,
    lastReview: 'December 15, 2024',
    nextReview: 'June 15, 2025',
    reviewer: 'Sarah Johnson',
    comments: 'Excellent performance with consistent delivery. Leadership qualities demonstrated.'
  };
  
  ngOnInit(): void {
    this.updateDateTime();
    // Update time every minute
    setInterval(() => {
      this.updateDateTime();
    }, 60000);
  }
  
  updateDateTime(): void {
    const now = new Date();
    this.currentDay = now.toLocaleDateString('en-US', { weekday: 'long' });
    this.currentDate = now.toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    });
    this.currentTime = now.toLocaleTimeString('en-US', { 
      hour: '2-digit', 
      minute: '2-digit',
      hour12: true
    });
  }
  
  navigateTo(section: string, id?: string): void {
    console.log(`Navigating to: ${section}`, id);
    alert(`🔍 Navigating to: ${section.toUpperCase()} ${id ? `- ${id}` : ''}\n\nThis would redirect to the respective details page.`);
  }
  
  getStars(rating: number): number[] {
    return Array(Math.floor(rating)).fill(0);
  }
  
  getEmptyStars(rating: number): number[] {
    return Array(5 - Math.floor(rating)).fill(0);
  }
}