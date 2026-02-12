import { Component, EventEmitter, Input, OnChanges, OnInit, Output, SimpleChanges } from '@angular/core';
import { CountryService } from '../services/country.service';
import { StateService } from '../services/state.service';
import { State } from '../models/state';
import { Country } from '../models/country';
import { response } from 'express';
import { forkJoin } from 'rxjs';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { City } from '../models/city';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-create-city',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './create-city.component.html',
  styleUrl: './create-city.component.css'
})
export class CreateCityComponent implements OnInit, OnChanges {

  states: State[] = [];

  @Input() isVisible: boolean = false;
  @Input() countries: Country[] = [];
  @Input() state: State[] = [];
  @Input() city: City | null = null;

  @Output() closeSidebar = new EventEmitter<void>();
  @Output() saveCity = new EventEmitter<City>();

  filteredStates: State[] = [];

  cityForm!: FormGroup;

  constructor(private countryService: CountryService, private stateService: StateService, private fb: FormBuilder) {
    this.cityForm = this.fb.group({
      ContryId: [null, [Validators.required]],
      StateId: [null, [Validators.required]],
      Name: ['', [Validators.required, Validators.maxLength(100)]],
      Code: ['', [Validators.required, Validators.maxLength(10)]]
    })
  }

  ngOnChanges(changes: SimpleChanges): void {

    if (changes['isVisible']?.currentValue === true) {

      if (this.city) {
        // edit mode → patch existing data
        this.patchForm(this.city);
      } else {
        // create mode → empty form
        this.resetForm();
      }
    }

    // When city input changes (edit clicked)
    if (changes['city'] && changes['city'].currentValue) {
      this.patchForm(changes['city'].currentValue);
    }


  }
  ngOnInit(): void {
    this.loadIntialData();
  }

  loadIntialData(): void {

    forkJoin({
      countries: this.countryService.getCountriesListAsync(),
      states: this.stateService.getStateListAsync()
    }).subscribe({
      next: ({ countries, states }) => {
        this.countries = countries;
        this.states = states;
      },
      error: (error) => {
        console.error('Error loading data:', error);
      }
    });
  }
  private resetForm(): void {
    this.cityForm.reset();
    this.cityForm.markAsPristine();
    this.cityForm.markAsUntouched();
  }
  close(): void {
    this.resetForm();
    this.closeSidebar.emit();

  }
  onSubmit(): void {
    if (this.cityForm.valid) {
      const citydata: City = {
        ...this.cityForm.value,
        Id: this.city?.Id || 0
      };

      this.saveCity.emit(citydata);
      this.resetForm();
    } else {
      // Mark all fields as touched to show validation errors
      this.cityForm.markAllAsTouched();
    }
  }

  private patchForm(city: City): void {
    this.cityForm.patchValue({
      ContryId: city.ContryId || '',
      StateId: city.StateId || '',
      Name: city.Name || '',
      Code: city.Code || ''
    }, { emitEvent: false });

    // Mark form as pristine after patching existing data
    if (city.Id) {
      this.cityForm.markAsPristine();
      this.cityForm.markAsUntouched();
    }
  }

  onCountryChange() {
    const countryId = this.cityForm.get('ContryId')?.value;

    console.log("countryId:", countryId);

    if (!countryId) return;

    this.loadStatesByCountry(Number(countryId));
  }

  loadStatesByCountry(countryId: number) {
    this.stateService.getStatesByCountry(countryId)
      .subscribe(res => {
        this.filteredStates = res;
      });
  }
}


