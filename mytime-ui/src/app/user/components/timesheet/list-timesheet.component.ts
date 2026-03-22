import { CommonModule } from '@angular/common';
import { Component, OnDestroy, OnInit } from '@angular/core';
import { AgGridAngular } from 'ag-grid-angular';

@Component({
  selector: 'app-list-timesheet',
  standalone: true,
  imports: [CommonModule, AgGridAngular],
  templateUrl: './list-timesheet.component.html',
  styleUrl: './list-timesheet.component.css'
})
export class ListTimesheetComponent implements OnInit, OnDestroy {
//list if taskcodes
//list of taskitenm
//list of timesheets for use
// list of tiemsheettasks for user
//InsertOrUpdateTimesheet
//remove timesheet

  ngOnDestroy(): void {

  }
  ngOnInit(): void {

  }
}
