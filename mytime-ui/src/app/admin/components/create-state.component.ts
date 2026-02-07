import { Component, EventEmitter, Input, OnChanges, Output, SimpleChanges } from '@angular/core';
import { Country } from '../models/country';
import { State } from '../models/state';
import { FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-create-state',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, FormsModule],
  templateUrl: './create-state.component.html',
  styleUrl: './create-state.component.css'
})
export class CreateStateComponent implements OnChanges {
  @Input() isVisible: boolean = false;
  @Input() countries: Country[] = [];
  @Input() state: State | null = null;

  @Output() closeSidebar = new EventEmitter<void>();
  @Output() saveState = new EventEmitter<State>();

  stateForm!: FormGroup;

  constructor(private fb: FormBuilder) {
    this.stateForm = this.fb.group({
      CountryId: [null, Validators.required],
      Name: ['', [Validators.required, Validators.maxLength(100)]],
      StateCode: ['', [Validators.required, Validators.maxLength(100)]],
      CountryCode: ['', [Validators.required, Validators.maxLength(100)]],
      Description: ['', [Validators.required, Validators.maxLength(100)]],
    });
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['state'] && this.state) {
      this.stateForm.patchValue({
        CountryId: this.state.CountryId,
        Name: this.state.Name,
        StateCode: this.state.StateCode,
        Description: this.state.Description,
      });
      this.populateCountryCode(this.state.CountryId);
    } else if (changes['state'] && !this.state) {
      this.stateForm.reset();
    }
  }

  close(): void {
    this.closeSidebar.emit();
  }

  onSubmit(): void {
    if (this.stateForm.valid) {
      const formValue = this.stateForm.value;
      const _state: State = {
        StateId: this.state?.StateId || 0,
        CountryCode: formValue.CountryCode,
        CountryId: formValue.CountryId,
        Name: formValue.Name,
        StateCode: formValue.StateCode,
        Description: formValue.Description,
      };
      this.saveState.emit(_state);
      // Optionally reset the form after save, or handle in parent component
      // this.stateForm.reset();
    } else {
      // Mark all fields as touched to show validation errors
      this.stateForm.markAllAsTouched();
    }
  }

  onCountrySelected(event: any): void {
    const selectedCountryId = event.target.value;
    console.log('Selected Country ID:', selectedCountryId);  
    const extractedId = typeof selectedCountryId === 'string' ? selectedCountryId.split(':')[1] : selectedCountryId;
    console.log('Extracted ID:', extractedId);
    this.populateCountryCode(extractedId);
  }

  private populateCountryCode(countryId: any): void {
    const selectedCountry = this.countries.filter(c => c.Id === parseInt(countryId))[0];
    if (selectedCountry) {
      this.stateForm.patchValue({
        CountryCode: selectedCountry.Code
      });
      console.log('Populated Country Code:', selectedCountry.Code);
    } else {
      this.stateForm.patchValue({
        CountryCode: ''
      });
      console.warn('No country found for ID:', countryId);
    }
  }
}