import { CommonModule } from '@angular/common';
import { Component, Input, OnDestroy, OnInit, HostListener } from '@angular/core';
import { AgGridAngular } from 'ag-grid-angular';
import { AllCommunityModule, ColDef, GridApi, GridOptions, ModuleRegistry, GridReadyEvent, ValueFormatterParams } from 'ag-grid-community';
import { EmployeeAddress } from '../../../models/employee_address';
import { ActionsRendererComponent } from '../../../../common/components/actions-renderer.component';
import { MobileActionsRendererComponent } from '../../../../common/components/mobile-actions-renderer.component';
import { EmployeeAddressService } from '../../../services/employee_address.service';
import { LoaderService } from '../../../../common/services/loader.service';
import { AuditFieldsService } from '../../../../common/services/auditfields.service';
import { ToastrService } from 'ngx-toastr';
import { CountryService } from '../../../services/country.service';
import { StateService } from '../../../services/state.service';
import { CityService } from '../../../services/city.service';
import { Country } from '../../../models/country';
import { State } from '../../../models/state';
import { City } from '../../../models/city';
import { forkJoin } from 'rxjs';
import { EmployeeAddressDetails } from '../../../models/employee_address_details';
import { EmployeesAddressesAddComponent } from './employees-addresses-add.component';

ModuleRegistry.registerModules([AllCommunityModule]);

@Component({
  selector: 'app-employees-addresses-list',
  standalone: true,
  imports: [CommonModule, AgGridAngular, EmployeesAddressesAddComponent],
  templateUrl: './employees-addresses-list.component.html',
  styleUrl: './employees-addresses-list.component.css'
})
export class EmployeesAddressesListComponent implements OnInit, OnDestroy {

  @Input() employeeId: number = 0;

  private employeesAddressesGridApi!: GridApi;

  isMobile: boolean = false;

  employeeAddress: EmployeeAddress[] = [];

  employeeAddressDetails: EmployeeAddressDetails[] = [];

  showEmployeeAddress = false;

  selectedEmployeeAddress: EmployeeAddress | null = null;

  desktopColumnDefs: ColDef[] = [
    {
      field: 'HNo',
      headerName: 'House No',
      width: 100,
      filter: 'agTextColumnFilter',
      sortable: true
    },
    {
      field: 'AddressLineOne',
      headerName: 'Address Line 1',
      width: 150,
      filter: 'agTextColumnFilter',
      sortable: true
    },
    {
      field: 'AddressLineTwo',
      headerName: 'Address Line 2',
      width: 150,
      filter: 'agTextColumnFilter',
      sortable: true
    },
    {
      field: 'Landmark',
      headerName: 'Landmark',
      width: 120,
      filter: 'agTextColumnFilter',
      sortable: true
    },
    {
      field: 'CityName',
      headerName: 'City',
      width: 120,
      filter: 'agTextColumnFilter',
      sortable: true
    },
    {
      field: 'StateName',
      headerName: 'State',
      width: 120,
      filter: 'agTextColumnFilter',
      sortable: true
    },
    {
      field: 'CountryName',
      headerName: 'Country',
      width: 120,
      filter: 'agTextColumnFilter',
      sortable: true
    },
    {
      field: 'Zipcode',
      headerName: 'Zip Code',
      width: 100,
      filter: 'agTextColumnFilter',
      sortable: true
    },
    {
      field: 'IsActive',
      headerName: 'Status',
      width: 100,
      filter: 'agTextColumnFilter',
      sortable: true,
      cellRenderer: (params: ValueFormatterParams) => {
        return params.value ? 'Active' : 'Inactive';
      },
      cellClass: (params: ValueFormatterParams) => {
        return params.value ? 'text-success' : 'text-danger';
      }
    },
    {
      field: 'Actions',
      headerName: 'Actions',
      width: 150,
      sortable: false,
      filter: false,
      cellRenderer: ActionsRendererComponent,
      cellRendererParams: {
        onEditClick: (data: any) => this.openEditEmployeeAddressForm(data),
        onDeleteClick: (data: any) => this.deleteEmployeeAddress(data)
      },
      cellClass: 'text-center',
      pinned: 'right'
    }
  ];

  mobileColumnDefs: ColDef[] = [
    {
      field: 'HNo',
      headerName: 'House No',
      width: 80
    },
    {
      field: 'AddressLineOne',
      headerName: 'Address',
      width: 150,
      cellRenderer: (params: ValueFormatterParams) => {
        const data = params.data as EmployeeAddressDetails;
        let address = params.value || '';
        if (data.CityName) {
          address += ', ' + data.CityName;
        }
        return address;
      }
    },
    {
      field: 'IsActive',
      headerName: 'Status',
      width: 80,
      cellRenderer: (params: ValueFormatterParams) => {
        return params.value ? 'Active' : 'Inactive';
      },
      cellClass: (params: ValueFormatterParams) => {
        return params.value ? 'text-success' : 'text-danger';
      }
    },
    {
      field: 'Actions',
      headerName: '',
      width: 80,
      sortable: false,
      filter: false,
      cellRenderer: MobileActionsRendererComponent,
      cellRendererParams: {
        onEditClick: (data: any) => this.openEditEmployeeAddressForm(data),
        onDeleteClick: (data: any) => this.deleteEmployeeAddress(data)
      },
      cellClass: 'text-center',
      pinned: 'right'
    }
  ];

  columnDefs: ColDef[] = [];

  defaultColDef: ColDef = {
    flex: 1,
    minWidth: 100,
    filter: true,
    resizable: true,
    sortable: true,
    floatingFilter: false
  };

  employeeAddressGridOptions: GridOptions = {
    pagination: true,
    paginationPageSize: 10,
    paginationPageSizeSelector: [10, 20, 50, 100],
    rowSelection: 'single',
    animateRows: true,
    enableCellTextSelection: true,
    suppressRowClickSelection: false,
    domLayout: 'autoHeight',
    overlayNoRowsTemplate: 'No addresses found'
  };

  private countriesMap: Map<number, string> = new Map();
  private statesMap: Map<number, string> = new Map();
  private citiesMap: Map<number, string> = new Map();

  coreCountries: Country[] = [];
  coreStates: State[] = [];
  coreCities: City[] = [];



  constructor(private employeeAddressService: EmployeeAddressService,
    private loader: LoaderService,
    private audit: AuditFieldsService,
    private toster: ToastrService,
    private countryService: CountryService,
    private stateService: StateService,
    private cityService: CityService
  ) { }

  ngOnDestroy(): void {
    window.removeEventListener('resize', this.onResize.bind(this));
  }

  ngOnInit(): void {
    this.checkScreenSize();
    this.setupResponsiveColumns();
    this.loadInitialData();
    window.addEventListener('resize', this.onResize.bind(this));
  }

  private loadInitialData(): void {
    this.loader.show();
    forkJoin({
      countries: this.countryService.getCountriesListAsync(),
      states: this.stateService.getStateListAsync(),
      cities: this.cityService.getCitiesListAsync(),
      employeeAddress: this.employeeAddressService.getEmployeeAddressListByEmployeeAsync(this.employeeId)
    }).subscribe({
      next: ({ countries, states, cities, employeeAddress }) => {
        this.coreCountries = countries;
        this.coreStates = states;
        this.coreCities = cities;
        this.employeeAddress = employeeAddress;

        // Process Country
        this.countriesMap.clear();
        countries.forEach(country => {
          this.countriesMap.set(country.Id, country.Name);
        });

        // Process States
        this.statesMap.clear();
        states.forEach(state => {
          this.statesMap.set(state.StateId, state.Name);
        });

        // Process Cities
        this.citiesMap.clear();
        cities.forEach(city => {
          this.citiesMap.set(city.Id, city.Name);
        });

        // Process and map employee addresses with lookup data
        this.employeeAddressDetails = employeeAddress.map(emp => {
          const address: EmployeeAddressDetails = {
            ...emp,
            CountryName: this.getCountryName(emp.CountryId ?? null),
            StateName: this.getStateName(emp.StateId ?? null),
            CityName: this.getCityName(emp.CityId ?? null)
          };
          return address;
        });

        this.loader.hide();

        // Update grid if ready
        if (this.employeesAddressesGridApi) {
          this.employeesAddressesGridApi.setGridOption('rowData', this.employeeAddressDetails);
          setTimeout(() => {
            this.employeesAddressesGridApi.sizeColumnsToFit();
          }, 100);
        }
      },
      error: (error) => {
        console.error('Error loading initial data:', error);
        this.loader.hide();
        this.toster.error('Failed to load address data');
      }
    });
  }

  private checkScreenSize(): void {
    const wasMobile = this.isMobile;
    this.isMobile = window.innerWidth < 768;

    if (wasMobile !== this.isMobile) {
      this.setupResponsiveColumns();
      if (this.employeesAddressesGridApi) {
        this.employeesAddressesGridApi.setGridOption('columnDefs', this.columnDefs);
      }
    }
  }

  private setupResponsiveColumns(): void {
    if (this.isMobile) {
      this.columnDefs = [...this.mobileColumnDefs];
      this.employeeAddressGridOptions.domLayout = 'autoHeight';
    } else {
      this.columnDefs = [...this.desktopColumnDefs];
      this.employeeAddressGridOptions.domLayout = 'normal';
    }
    if (this.employeesAddressesGridApi) {
      this.refreshGridColumns();
    }
  }

  onGridReady(params: GridReadyEvent): void {
    this.employeesAddressesGridApi = params.api;
    if (this.employeeAddressDetails.length > 0) {
      this.employeesAddressesGridApi.setGridOption('rowData', this.employeeAddressDetails);
    }

    setTimeout(() => {
      this.employeesAddressesGridApi.sizeColumnsToFit();
    }, 300);
  }

  @HostListener('window:resize')
  onResize(): void {
    this.checkScreenSize();
  }

  refreshData(): void {
    this.loadInitialData();
  }

  private refreshGridColumns(): void {
    if (!this.employeesAddressesGridApi) return;
    setTimeout(() => {
      this.employeesAddressesGridApi.refreshHeader();
      this.employeesAddressesGridApi.sizeColumnsToFit();
    }, 100);
  }

  closeAddressForm(): void {
    this.showEmployeeAddress = false;
    this.selectedEmployeeAddress = null;
  }

  openAddAddressForm(): void {
    this.showEmployeeAddress = true;
    this.selectedEmployeeAddress = null;
  }
  onAddressSave(employeeAddress: EmployeeAddress): void {
    console.log(employeeAddress);

    var _address = this.audit.appendAuditFields(employeeAddress);
    console.log(_address);

    this.loader.show();
    this.employeeAddressService.insertOrUpdateEmployeeAddressAsync(_address).subscribe({
      next: (response) => {
        if (response) {
          this.toster.success('Address saved successfully');
          this.closeAddressForm();
          this.refreshData();
        }
      },
      error: (error) => {
        console.error('Error saving education:', error);
        this.toster.error('Failed to save education');
        this.loader.hide();
      }
    });


  }

  openEditEmployeeAddressForm(employeeAddress: EmployeeAddressDetails): void {
    this.selectedEmployeeAddress = employeeAddress;
    this.showEmployeeAddress = true;
    // Implement your edit logic here or emit event to parent
    console.log('Edit address:', employeeAddress);
  }

  deleteEmployeeAddress(employeeAddress: EmployeeAddressDetails): void {
    if (confirm('Are you sure you want to delete this address?')) {
      // Implement your delete logic here
      console.log('Delete address:', employeeAddress);
    }
  }
  getTotalRowsCount(): number {
    return this.employeeAddressDetails.length;
  }

  getActiveAddressesCount(): number {
    return this.employeeAddressDetails.filter(x => x.IsActive == true).length;
  }

  private getCountryName(countryId: number | null | undefined): string {
    if (countryId === null || countryId === undefined) return 'N/A';
    return this.countriesMap.get(countryId) || 'Unknown Country';
  }

  private getStateName(stateId: number | null | undefined): string {
    if (stateId === null || stateId === undefined) return 'N/A';
    return this.statesMap.get(stateId) || 'Unknown State';
  }

  private getCityName(cityId: number | null | undefined): string {
    if (cityId === null || cityId === undefined) return 'N/A';
    return this.citiesMap.get(cityId) || 'Unknown City';
  }
}