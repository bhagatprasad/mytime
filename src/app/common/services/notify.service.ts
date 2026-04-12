import { Injectable } from '@angular/core';
import { ToastrService } from 'ngx-toastr';

@Injectable({ providedIn: 'root' })
export class NotifyService {
  constructor(private toastr: ToastrService) { }

  showSuccess(message: string, title?: string) {
    this.toastr.success(message, title, {
      timeOut: 3000,
      progressBar: true,
      progressAnimation: 'decreasing'
    });
  }

  showError(message: string, title?: string) {
    this.toastr.error(message, title, {
      timeOut: 3000,
      progressBar: true,
      progressAnimation: 'decreasing'
    });
  }

  showInfo(message: string, title?: string) {
    this.toastr.info(message, title, {
      timeOut: 3000,
      progressBar: true,
      progressAnimation: 'decreasing'
    });
  }

  showWarning(message: string, title?: string) {
    this.toastr.warning(message, title,
      {
        timeOut: 3000,
        progressBar: true,
        progressAnimation: 'decreasing'
      }
    );
  }
}