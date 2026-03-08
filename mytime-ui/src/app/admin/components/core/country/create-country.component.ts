import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, OnChanges, Output, SimpleChanges, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { Country } from '../../../models/country';

@Component({
  selector: 'app-create-country',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule],
  templateUrl: './create-country.component.html',
  styleUrls: ['./create-country.component.css']
})
export class CreateCountryComponent implements OnChanges, OnInit {

  @Input() isVisible: boolean = false;
  @Input() country: Country | null = null;
  
  @Output() closeSidebar = new EventEmitter<void>();
  @Output() saveCountry = new EventEmitter<Country>();

  countryForm: FormGroup;

  constructor(private fb: FormBuilder) {
    this.countryForm = this.fb.group({
      Name: ['', [Validators.required, Validators.maxLength(100)]],
      Code: ['', [Validators.required, Validators.maxLength(10)]]
    });
  }

  ngOnInit(): void {
    if (this.country) {
      this.patchForm(this.country);
    }
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['isVisible'] && changes['isVisible'].currentValue) {
      this.resetForm();
      if (this.country) {
        this.patchForm(this.country);
      }
    }
    
    if (changes['country']) {
      const country = changes['country'].currentValue;
      if (country) {
        this.patchForm(country);
      } else {
        this.resetForm();
      }
    }
  }

  private patchForm(country: Country): void {
    this.countryForm.patchValue({
      Name: country.Name || '',
      Code: country.Code || ''
    });
  }

  private resetForm(): void {
    this.countryForm.reset();
    this.countryForm.markAsPristine();
    this.countryForm.markAsUntouched();
  }

  close(): void {
    this.resetForm();
    this.closeSidebar.emit();
  }

  onSubmit(): void {
    if (this.countryForm.valid) {
      const countryData: Country = {
        ...this.countryForm.value,
        Id: this.country?.Id || 0
      };
      
      this.saveCountry.emit(countryData);
      this.resetForm();
    } else {
      this.countryForm.markAllAsTouched();
    }
  }
}