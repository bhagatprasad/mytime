import { Component, OnChanges, OnInit, SimpleChanges } from '@angular/core';
import { CountryService } from '../services/country.service';
import { StateService } from '../services/state.service';
import { State } from '../models/state';
import { Country } from '../models/country';
import { response } from 'express';
import { forkJoin } from 'rxjs';

@Component({
  selector: 'app-create-city',
  standalone: true,
  imports: [],
  templateUrl: './create-city.component.html',
  styleUrl: './create-city.component.css'
})
export class CreateCityComponent implements OnInit, OnChanges {

  states: State[] = [];

  countries: Country[] = [];

  constructor(private countryService: CountryService, private stateService: StateService) { }

  ngOnChanges(changes: SimpleChanges): void {

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
}
