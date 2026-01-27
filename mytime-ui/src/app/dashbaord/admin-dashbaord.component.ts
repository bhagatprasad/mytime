import { Component, OnInit } from '@angular/core';
import { LoaderService } from '../common/services/loader.service';
import { NotifyService } from '../common/services/notify.service';

@Component({
  selector: 'app-admin-dashbaord',
  standalone: true,
  imports: [],
  templateUrl: './admin-dashbaord.component.html',
  styleUrl: './admin-dashbaord.component.css'
})
export class AdminDashbaordComponent implements OnInit {
  constructor(private loader: LoaderService,
    private notify: NotifyService
  ) {

  }
  ngOnInit(): void {

  }
  loadDashboardData() {
    this.loader.show();
    console.log("hello");
    setTimeout(() => {
      this.loader.hide();
      this.notify.showSuccess("Hiiii");
    }, 200000);
  }
}
