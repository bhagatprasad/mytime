import { Component, input, OnInit } from '@angular/core';
import { FullCalendarModule } from '@fullcalendar/angular';
import dayGridPlugin from '@fullcalendar/daygrid';
import interactionPlugin from '@fullcalendar/interaction';
import { HolydayCallenderService } from '../../../admin/services/HolydayCallender.service';
import multiMonthPlugin from '@fullcalendar/multimonth';
import timeGridPlugin from '@fullcalendar/timegrid';
import { AuditFieldsService } from '../../../common/services/auditfields.service';
import { LoaderService } from '../../../common/services/loader.service';
import { HolidayCallender } from '../../../admin/models/HolidayCallender';
import { CommonModule } from '@angular/common';
import { ViewChild, ElementRef } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { FullCalendarComponent } from '@fullcalendar/angular';


@Component({
  selector: 'app-holidaycalender',
  standalone: true,
  imports: [FullCalendarModule, CommonModule, FormsModule],
  templateUrl: './holidaycalendar.component.html',
  styleUrl: './holidaycalendar.component.css'
})
export class HolidaycalendarComponent implements OnInit {

  constructor(private holidayservice: HolydayCallenderService, private audit: AuditFieldsService, private loader: LoaderService) { }

  showPopup = false;
  selectedDate: string = '';
  holidayName: string = '';

  calendarOptions: any = {

    plugins: [dayGridPlugin, interactionPlugin, multiMonthPlugin, timeGridPlugin],

    initialView: 'dayGridMonth',

    events: [],

    dateClick: this.openAddHolidayPopup.bind(this),

    height: 'auto',
    contentHeight: 'auto',

    headerToolbar: {
      left: 'prev,next today',
      center: 'title',
      right: ''
    },
    views: {
      multiMonthYear: {
        type: 'multiMonth',
        duration: { years: 1 },
        buttonText: 'Year',
      }
    },
  };

  ngOnInit() {

    this.loadHolidaycalender();
  }
  @ViewChild('holidayInput') holidayInput!: ElementRef;
  @ViewChild('calendar') calendarComponent!: FullCalendarComponent;

  loadHolidaycalender(): void {
  //  this.loader.show();
    this.holidayservice.getHolydaysListAsync()
      .subscribe(data => {

        this.calendarOptions.events = data.map((x: any) => ({
          title: x.FestivalName,
          date: x.HolidayDate.split('T')[0]

        }));
// this.loader.hide();
      });
  }

  changeView(event: any) {

    const view = event.target.value;

    this.calendarComponent.getApi().changeView(view);

  }

  openAddHolidayPopup(info: any) {
    this.selectedDate = info.dateStr;
    this.holidayName = '';
    this.showPopup = true;
    setTimeout(() => {
      this.holidayInput?.nativeElement.focus();
    }, 0);
  }

  saveHoliday() {

    const holiday: HolidayCallender = {
      FestivalName: this.holidayName,
      HolidayDate: this.selectedDate
    } as any;

    this.handleDateClick(holiday);

    this.showPopup = false;
    this.holidayName = '';
  }

  handleDateClick(holiday: HolidayCallender): void {

    this.loader.show();

    var _holiday = this.audit.appendAuditFields(holiday);

    this.holidayservice.insertOrUpdateHolidayCallender(_holiday).subscribe(
      (response) => {
        if (response) {
          this.loadHolidaycalender();
        }
        this.loader.hide();
      },
      (error) => {
        this.loader.hide();
      }
    );
  }
}