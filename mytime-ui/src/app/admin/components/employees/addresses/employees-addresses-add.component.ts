import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, OnChanges, Output, SimpleChanges } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { EmployeeAddress } from '../../../models/employee_address';
import { Country } from '../../../models/country';
import { State } from '../../../models/state';
import { StateService } from '../../../services/state.service';
import { CityService } from '../../../services/city.service';
import { City } from '../../../models/city';

@Component({
  selector: 'app-employees-addresses-add',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './employees-addresses-add.component.html',
  styleUrl: './employees-addresses-add.component.css'
})
export class EmployeesAddressesAddComponent implements OnChanges {

  @Input() employeeAddress: EmployeeAddress | null = null;
  @Input() isVisible: boolean = false;
  @Input() employeeId: number = 0;
  @Input() countries:Country[] = [];
  @Input() states :State[] = [];
  @Input() cities :City[] = [];

  @Output() save = new EventEmitter<EmployeeAddress>();
  @Output() close = new EventEmitter<void>();

  addressForm: FormGroup;

  constructor(private fb: FormBuilder ,private stateservice:StateService, private cityservice:CityService) {
    this.addressForm = this.fb.group({
      EmployeeAddressId: [0],
      EmployeeId: [this.employeeId],
      HNo: ['', Validators.required],
      AddressLineOne: ['', Validators.required],
      AddressLineTwo: ['', [Validators.required]],
      Landmark: ['', [Validators.required]],
      CountryId: [null, [Validators.required]],
      StateId: [null, [Validators.required]],
      CityId: [null, [Validators.required]],
      Zipcode: [null, [Validators.required]],
      IsActive: [true]

    });

  }
  ngOnChanges(changes: SimpleChanges): void {
    if (changes['isVisible']?.currentValue === true) {

      if (this.employeeAddress) {
        // edit mode → patch existing data
        this.patchForm(this.employeeAddress);
      } else {
        // create mode → empty form
        this.resetForm();
      }
    }

    if (changes['employeeAdress'] && changes['employeeAdress'].currentValue) {
      this.patchForm(changes['employeeAdress'].currentValue);
    }

  }

  private resetForm(): void {
    this.addressForm.reset();
    this.addressForm.markAsPristine();
    this.addressForm.markAsUntouched();
  }
  onClose(): void {
    this.resetForm();
    this.close.emit();

  }

  private patchForm(address: EmployeeAddress): void {
    this.addressForm.patchValue({
      HNo: address.HNo || '',
      AddressLineOne: address.AddressLineOne || '',
      AddressLineTwo: address.AddressLineTwo || '',
      Landmark: address.Landmark || '',
      CountryId: address.CountryId || '',
      StateId: address.StateId || '',
      CityId: address.CityId || '',
      Zipcode: address.Zipcode || ''
    }, { emitEvent: false });

    // Mark form as pristine after patching existing data
    if (address.EmployeeAddressId) {
      this.addressForm.markAsPristine();
      this.addressForm.markAsUntouched();
    }
  }
  onSubmit(): void {
    if (this.addressForm.valid) {
      const formValue = this.addressForm.value;
      const _address: EmployeeAddress = {
        EmployeeAddressId: this.employeeAddress?.EmployeeAddressId|| 0,
        EmployeeId: this.employeeId,
        HNo: formValue.HNo,
        AddressLineOne: formValue.AddressLineOne,
        AddressLineTwo: formValue.AddressLineTwo,
        Landmark: formValue.Landmark,
        CountryId:formValue.CountryId,
        StateId:formValue.StateId,
        CityId:formValue.CityId,
        Zipcode:formValue.Zipcode,
      };
      this.save.emit(_address);
      // Optionally reset the form after save, or handle in parent component
      // this.stateForm.reset();
    } else {
      // Mark all fields as touched to show validation errors
      this.addressForm.markAllAsTouched();
    }
  }

  onCountryChange() {
    const countryId = this.addressForm.get('CountryId')?.value;

    console.log("countryId:", countryId);

    if (!countryId) return;

    this.loadStatesByCountry(Number(countryId));
  }
  loadStatesByCountry(countryId: number) {
    this.stateservice.getStatesByCountry(countryId)
    .subscribe(res => {
        this.states = res;
      });
  }

  onStateChange() {
    const stateId = this.addressForm.get('StateId')?.value;

    console.log("StateId:", stateId);

    if (!stateId) return;

    this.loadcityBystate(Number(stateId));
  }

  loadcityBystate(stateId: number) {
    this.cityservice.getCitiesListByStateAsync(stateId)
    .subscribe(res => {
        this.cities = res;
      });
  }
}
