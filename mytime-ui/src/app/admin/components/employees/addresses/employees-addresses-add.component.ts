import { CommonModule } from '@angular/common';
import { Component, EventEmitter, Input, OnChanges, Output, SimpleChanges } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { EmployeeAddress } from '../../../models/employee_address';

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

  @Output() save = new EventEmitter<EmployeeAddress>();
  @Output() close = new EventEmitter<void>();

  addressForm: FormGroup;

  constructor(private fb: FormBuilder) {
    this.addressForm = this.fb.group({
      EmployeeAddressId: [0],
      EmployeeId: [this.employeeId],
      HNo: ['', Validators.required],
      AddressLineOne: ['', Validators.required],
      AddressLineTwo: ['', [Validators.required]],
      Landmark: ['', [Validators.required]],
      IsActive: [true]

    });

  }
  ngOnChanges(changes: SimpleChanges): void {

  }
  onClose(): void {

  }
  onSubmit(): void {
    console.log("save clicked");

    if (this.addressForm.valid) {
      const formValue = this.addressForm.value;

      const address: EmployeeAddress = {
        EmployeeAddressId: 0,
        AddressLineOne: formValue.AddressLineOne,
        AddressLineTwo: formValue.AddressLineTwo,
        HNo: formValue.HNo,
        Landmark: formValue.Landmark,
        EmployeeId: this.employeeId
      };
      this.save.emit(address);
    }

  }
}
