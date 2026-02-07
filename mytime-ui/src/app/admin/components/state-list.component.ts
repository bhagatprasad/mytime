import { CommonModule, DatePipe } from '@angular/common';
import { Component, HostListener, OnDestroy, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { AgGridAngular } from 'ag-grid-angular';
import { AllCommunityModule, ColDef, GridApi, GridOptions, GridReadyEvent, ICellRendererParams, ModuleRegistry, ValueFormatterParams } from 'ag-grid-community';
import { Country } from '../models/country';
import { State } from '../models/state';
import { StateService } from '../services/state.service';
import { CountryService } from '../services/country.service';
import { LoaderService } from '../../common/services/loader.service';
import { ToastrService } from 'ngx-toastr';
import { AuditFieldsService } from '../../common/services/auditfields.service';
import { ActionsRendererComponent } from '../../common/components/actions-renderer.component';
import { MobileActionsRendererComponent } from '../../common/components/mobile-actions-renderer.component';
import { forkJoin } from 'rxjs';
import { DeleteConfirmationComponent } from '../../common/components/delete.compunent';
import { CreateStateComponent } from './create-state.component';

ModuleRegistry.registerModules([AllCommunityModule]);

@Component({
  selector: 'app-state-list',
  standalone: true,
  imports: [CommonModule, AgGridAngular, DatePipe, FormsModule, DeleteConfirmationComponent, CreateStateComponent],
  templateUrl: './state-list.component.html',
  styleUrl: './state-list.component.css'
})
export class StateListComponent implements OnInit, OnDestroy {

  today = new Date();

  countries: Country[] = [];

  states: State[] = [];

  showDeletePopup: boolean = false;

  selectedDeleteItem: State | null = null;

  private gridApi!: GridApi;

  isMobile: boolean = false;

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

  desktopColumnDefs: ColDef[] = [
    {
      field: 'StateId',
      headerName: 'ID',
      width: 80,
      filter: 'agNumberColumnFilter',
      sortable: true,
      cellClass: 'text-center'
    },
    {
      field: 'Name',
      headerName: 'Name',
      width: 120,
      filter: 'agTextColumnFilter',
      sortable: true,
      cellRenderer: this.nameRenderer.bind(this)
    },
    {
      field: 'SateCode',
      headerName: 'Code',
      width: 120,
      filter: 'agTextColumnFilter',
      sortable: true,
      cellClass: 'text-center'
    },
    {
      field: 'CountryCode',
      headerName: 'Country',
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
        onEditClick: (data: any) => this.requestStateProcess(data),
        onDeleteClick: (data: any) => this.deleteState(data)
      },
      cellClass: 'text-center'
    }
  ];

  mobileColumnDefs: ColDef[] = [
    {
      field: 'Name',
      headerName: 'State',
      width: 180,
      cellRenderer: this.mobileNameRenderer.bind(this)
    },
    {
      field: 'Description',
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
        onEditClick: (data: any) => this.requestStateProcess(data)
      },
      cellClass: 'text-center'
    }
  ];

  showSidebar: boolean = false;

  selectedState: State | null = null;
  constructor(private stateService: StateService,
    private countryService: CountryService,
    private loader: LoaderService,
    private toster: ToastrService,
    private audit: AuditFieldsService) {

  }
  deleteState(state: State): void {
    this.showDeletePopup = true;
    this.selectedDeleteItem = state;
  }
  requestStateProcess(state: State): void {
  }

  loadRoleData(): void {
    this.loader.show();
    forkJoin({
      countries: this.countryService.getCountriesListAsync(),
      states: this.stateService.getStateListAsync()
    }).subscribe({
      next: ({ countries, states }) => {
        this.countries = countries;
        this.states = states;
        this.loader.hide();
        if (this.gridApi) {
          setTimeout(() => {
            this.gridApi.sizeColumnsToFit();
          }, 100);
        }
      },
      error: (error) => {
        console.error('Error loading data:', error);
        this.loader.hide();
        this.toster.error('Failed to load data', 'Error');
      }
    });
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


  getSelectedRowsCount(): number {
    return this.gridApi?.getSelectedRows()?.length || 0;
  }

  getTotalRowsCount(): number {
    return this.states.length;
  }

  getActiveStatesCount(): number {
    return this.states.filter(c => c.IsActive).length;
  }

  getInactiveStatesCount(): number {
    return this.states.filter(c => !c.IsActive).length;
  }

  closePopup() {
    this.showDeletePopup = false;
    this.selectedDeleteItem = null;
  }

  confirmDelete() {

    if (!this.selectedDeleteItem) {
      console.error("No item selected for delete");
      return;
    }

    this.stateService.deleteStateAsync(this.selectedDeleteItem.StateId)
      .subscribe({
        next: (res) => {
          console.log("Delete success:", res);

          this.refreshData();          // reload grid data
          this.showDeletePopup = false;
          this.selectedDeleteItem = null;
        },

        error: (err) => {
          console.error("Delete failed:", err);
          // keep popup open OR close — your choice
          this.showDeletePopup = false;

        },
        complete: () => {
          alert("Delete request completed");
        }
      });
  }
  refreshData() {
    this.loadRoleData();
  }

  onCloseSidebar(): void {
    this.showSidebar = false;
    this.selectedState = null;
  }

  onSaveState(state: State): void {
    this.loader.show();
    console.log(state);
    const _state = this.audit.appendAuditFields(state);
    this.stateService.insertOrUpdateStateAsync(_state).subscribe(reponse => {
      if (reponse) {
        this.toster.success("state processed succeessfully");
        this.showSidebar = false;
        this.refreshData();
      }
    }, error => {
      this.toster.error("something went wrong , please check and resubmit");
      this.showSidebar = true;
      this.loader.hide();
    });
  }
  openAddEditState(): void {
    this.showSidebar = true;
    this.selectedState = null;
  }

}
