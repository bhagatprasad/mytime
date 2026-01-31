import { Component, HostListener, OnDestroy, OnInit } from '@angular/core';
import { CountryService } from '../services/country.service';
import { LoaderService } from '../../common/services/loader.service';
import { AuditFieldsService } from '../../common/services/auditfields.service';
import { Country } from '../models/country';
import { AllCommunityModule, ColDef, GridApi, GridOptions, GridReadyEvent, ICellRendererParams, ModuleRegistry, ValueFormatterParams } from 'ag-grid-community';
import { CreateCountryComponent } from './create-country.component';
import { FormsModule } from '@angular/forms';
import { CommonModule, DatePipe } from '@angular/common';
import { AgGridAngular } from 'ag-grid-angular';
import { ActionsRendererComponent } from '../../common/components/actions-renderer.component';
import { MobileActionsRendererComponent } from '../../common/components/mobile-actions-renderer.component';
import { ToastrService } from 'ngx-toastr';


// Register AG Grid modules
ModuleRegistry.registerModules([AllCommunityModule]);


@Component({
  selector: 'app-country-list',
  standalone: true,
  imports: [CommonModule, AgGridAngular, DatePipe, FormsModule, CreateCountryComponent],
  templateUrl: './country-list.component.html',
  styleUrl: './country-list.component.css'
})
export class CountryListComponent implements OnInit, OnDestroy {

  countries: Country[] = [];

  today = new Date();

  private gridApi!: GridApi;

  isMobile: boolean = false;

  desktopColumnDefs: ColDef[] = [
    {
      field: 'Id',
      headerName: 'ID',
      width: 80,
      filter: 'agNumberColumnFilter',
      sortable: true,
      cellClass: 'text-center'
    },
    {
      field: 'Name',
      headerName: 'Country Name',
      width: 120,
      filter: 'agTextColumnFilter',
      sortable: true,
      cellRenderer: this.nameRenderer.bind(this)
    },
    {
      field: 'Code',
      headerName: 'Country Code',
      width: 120,
      filter: 'agTextColumnFilter',
      sortable: true,
      cellClass: 'text-center'
    },
    {
      field: 'IsActive',
      headerName: 'Status',
      width: 120,
      filter: 'agTextColumnFilter',
      sortable: true,
      cellRenderer: this.statusRenderer.bind(this),
      cellClass: this.statusCellClass.bind(this)
    },
    {
      field: 'CreatedBy',
      headerName: 'Created By',
      width: 120,
      filter: 'agNumberColumnFilter',
      sortable: true,
      cellClass: 'text-center'
    },
    {
      field: 'CreatedOn',
      headerName: 'Created Date',
      width: 120,
      filter: 'agDateColumnFilter',
      sortable: true,
      valueFormatter: this.dateFormatter.bind(this),
      cellClass: 'text-center'
    },
    {
      field: 'ModifiedBy',
      headerName: 'Modified By',
      width: 120,
      filter: 'agNumberColumnFilter',
      sortable: true,
      cellClass: 'text-center'
    },
    {
      field: 'ModifiedOn',
      headerName: 'Last Modified',
      width: 120,
      filter: 'agDateColumnFilter',
      sortable: true,
      valueFormatter: this.dateFormatter.bind(this),
      cellClass: 'text-center'
    },
    {
      field: 'Actions',
      headerName: 'Actions',
      width: 150,
      sortable: false,
      filter: false,
      cellRenderer: ActionsRendererComponent,
      cellRendererParams: {
        onEditClick: (data: any) => this.requestCountryProcess(data),
        onDeleteClick: (data: any) => this.deleteCountry(data)
      },
      cellClass: 'text-center'
    }
  ];

  mobileColumnDefs: ColDef[] = [
    {
      field: 'Name',
      headerName: 'Country',
      width: 180,
      cellRenderer: this.mobileNameRenderer.bind(this)
    },
    {
      field: 'Code',
      headerName: 'Code',
      width: 100,
      cellClass: 'text-center'
    },
    {
      field: 'Actions',
      headerName: '',
      width: 80,
      sortable: false,
      filter: false,
      cellRenderer: MobileActionsRendererComponent,
      cellRendererParams: {
        onEditClick: (data: any) => this.requestCountryProcess(data)
      },
      cellClass: 'text-center'
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

  gridOptions: GridOptions = {
    pagination: true,
    paginationPageSize: 10,
    paginationPageSizeSelector: [10, 20, 50, 100],
    rowSelection: 'single',
    animateRows: true,
    enableCellTextSelection: true,
    suppressRowClickSelection: false,
    domLayout: 'autoHeight'
  };

  showSidebar: boolean = false;

  selectedCountry: Country | null = null;

  constructor(private countryService: CountryService, private loader: LoaderService, private notify: ToastrService, private audit: AuditFieldsService) {

  }

  ngOnDestroy(): void {
    window.removeEventListener('resize', this.onResize.bind(this));
  }
  ngOnInit(): void {
    this.checkScreenSize();
    this.setupResponsiveColumns();
    this.loadRoleData();
    window.addEventListener('resize', this.onResize.bind(this));
  }
  private checkScreenSize(): void {
    const wasMobile = this.isMobile;
    this.isMobile = window.innerWidth < 768;

    if (wasMobile !== this.isMobile) {
      this.setupResponsiveColumns();
    }
  }

  private setupResponsiveColumns(): void {
    if (this.isMobile) {
      this.columnDefs = [...this.mobileColumnDefs];
      this.gridOptions.domLayout = 'autoHeight';
    } else {
      this.columnDefs = [...this.desktopColumnDefs];
      this.gridOptions.domLayout = 'normal';
    }
    if (this.gridApi) {
      this.refreshGridColumns();
    }
  }

  private refreshGridColumns(): void {
    if (!this.gridApi) return;
    const newColumnDefs = JSON.parse(JSON.stringify(this.columnDefs));
    setTimeout(() => {
      this.gridApi.refreshHeader();
      this.gridApi.sizeColumnsToFit();
    }, 100);
  }

  loadRoleData(): void {
    this.loader.show();

    this.countryService.getCountriesListAsync().subscribe({
      next: (countrys: Country[]) => {
        this.countries = countrys;
        this.loader.hide();
        if (this.gridApi) {
          setTimeout(() => {
            this.gridApi.sizeColumnsToFit();
          }, 100);
        }
      },
      error: (error) => {
        console.error('Error loading roles:', error);
        this.loader.hide();

        this.notify.error('Failed to load roles', 'Error');
      }
    });
  }

  onGridReady(params: GridReadyEvent): void {
    this.gridApi = params.api;
    setTimeout(() => {
      this.gridApi.sizeColumnsToFit();
    }, 300);
  }

  @HostListener('window:resize', ['$event'])
  onResize(event: any): void {
    this.checkScreenSize();
  }


  refreshData(): void {
    this.loadRoleData();
  }


  deleteCountry(country: Country): void {

  }

  requestCountryProcess(country: Country): void {
    this.selectedCountry = country;
    this.showSidebar = true;
  }
  openAddEditCountry() {
    this.showSidebar = true;
    this.selectedCountry = null;
  }
  onCloseSidebar() {
    this.showSidebar = false;
    this.selectedCountry = null;
  }
  onSaveCountry(country: Country) {
    this.loader.show();
    var _country = this.audit.appendAuditFields(country);
    console.log("we have receved countrt data " + JSON.stringify(_country));
    this.countryService.insertOrUpdateCountry(_country).subscribe(
      reponse => {
        if (reponse) {
          this.notify.success("country processed succeessfully");
          this.showSidebar = false;
          this.refreshData();
        }
      }, error => {
        this.notify.error("something went wrong , please check and resubmit");
        this.showSidebar = true;
        this.loader.hide();
      });
  }

  getSelectedRowsCount(): number {
    return this.gridApi?.getSelectedRows()?.length || 0;
  }

  getTotalRowsCount(): number {
    return this.countries.length;
  }

  getActiveCountriesCount(): number {
    return this.countries.filter(c => c.IsActive).length;
  }

  getInactiveCountriesCount(): number {
    return this.countries.filter(c => !c.IsActive).length;
  }

  nameRenderer(params: ICellRendererParams): string {
    return `
      <div class="role-name-cell">
        <strong>${params.value}</strong>
        <div class="text-muted small">Code: ${params.data.Code}</div>
      </div>
    `;
  }

  mobileNameRenderer(params: ICellRendererParams): string {
    return `
      <div class="mobile-role-cell">
        <strong>${params.value}</strong>
        <div class="text-muted small">ID: ${params.data.Id}</div>
      </div>
    `;
  }


  statusCellClass(params: any): string {
    const isActive = params.value;
    return isActive ? 'status-active' : 'status-inactive';
  }


  dateFormatter(params: ValueFormatterParams): string {
    if (!params.value) return 'N/A';

    const date = new Date(params.value);
    if (isNaN(date.getTime())) return 'Invalid Date';

    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  }


  statusRenderer(params: ICellRendererParams): string {
    const isActive = params.value;
    const statusText = isActive ? 'Active' : 'Inactive';
    const statusClass = isActive ? 'success' : 'danger';
    const icon = isActive ? 'mdi-check-circle' : 'mdi-close-circle';

    return `
          <div class="d-flex align-items-center gap-2">
            <i class="mdi ${icon} text-${statusClass}"></i>
            <span class="badge bg-${statusClass}">${statusText}</span>
          </div>
        `;
  }

  mobileStatusRenderer(params: ICellRendererParams): string {
    const isActive = params.value;
    const statusText = isActive ? 'Active' : 'Inactive';
    const statusClass = isActive ? 'success' : 'danger';

    return `<span class="badge bg-${statusClass}">${statusText}</span>`;
  }

}
