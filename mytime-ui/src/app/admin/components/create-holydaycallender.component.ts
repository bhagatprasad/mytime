import { Component, EventEmitter, Input, Output, SimpleChanges } from '@angular/core';
import { HolidayCallender } from '../models/HolidayCallender';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-create-holydaycallender',
  standalone: true,
  imports: [CommonModule,ReactiveFormsModule],
  templateUrl: './create-holydaycallender.component.html',
  styleUrl: './create-holydaycallender.component.css'
})
export class CreateHolydaycallenderComponent {

  @Input() isVisible: boolean = false;
  @Input() holidaycallender: HolidayCallender | null = null;

  @Output() closeSidebar = new EventEmitter<void>();
  @Output() saveHolidaycallender = new EventEmitter<HolidayCallender>();

  holidayForm: FormGroup;

  constructor(private fb: FormBuilder) {
    this.holidayForm = this.fb.group({
      FestivalName: ['', [Validators.required, Validators.maxLength(100)]],
      HolidayDate: ['', [Validators.required, Validators.maxLength(50)]],
      Year: ['', [Validators.required, Validators.maxLength(10)]]
    });
  }

  ngOnInit(): void {
    // If role is provided on initialization, patch the form
    if (this.holidaycallender) {
      this.patchForm(this.holidaycallender);
    }
  }

  ngOnChanges(changes: SimpleChanges): void {
    // Handle visibility changes
    if (changes['isVisible'] && changes['isVisible'].currentValue) {
      // Reset form when sidebar becomes visible for new holiday
      if (!this.holidaycallender?.Id) {
        this.resetForm();
      }

      // If holiday data is provided, patch it
      if (this.holidaycallender) {
        this.patchForm(this.holidaycallender);
      }
    }

    // Handle holiday input changes
    if (changes['holidaycallender']) {
      const holidaycallender = changes['holidaycallender'].currentValue;
      if (holidaycallender) {
        this.patchForm(holidaycallender);
      } else if (!this.isVisible) {
        this.resetForm();
      }
    }
  }

  private patchForm(holiday: HolidayCallender): void {
    this.holidayForm.patchValue({
      FestivalName: holiday.FestivalName || '',
      HolidayDate: holiday.HolidayDate || '',
      Year: holiday.Year || ''
    }, { emitEvent: false });

    // Mark form as pristine after patching existing data
    if (holiday.Id) {
      this.holidayForm.markAsPristine();
      this.holidayForm.markAsUntouched();
    }
  }

  private resetForm(): void {
    this.holidayForm.reset();
    this.holidayForm.markAsPristine();
    this.holidayForm.markAsUntouched();
  }

  close(): void {
    this.resetForm();
    this.closeSidebar.emit();
  }

  onSubmit(): void {
      if (this.holidayForm.valid) {
        const holidaydata: HolidayCallender = {
          ...this.holidayForm.value,
          Id: this.holidaycallender?.Id || 0
        };
        
        this.saveHolidaycallender.emit(holidaydata);
        this.resetForm();
      } else {
        // Mark all fields as touched to show validation errors
        this.holidayForm.markAllAsTouched();
      }
    }

}
