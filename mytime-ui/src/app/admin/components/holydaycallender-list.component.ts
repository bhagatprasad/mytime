import { Component, HostListener } from '@angular/core';
import { AllCommunityModule, ColDef, GridApi, GridOptions, GridReadyEvent, ICellRendererParams, ModuleRegistry, ValueFormatterParams } from 'ag-grid-community';
import { HolidayCallender } from '../models/HolidayCallender';
import { ActionsRendererComponent } from '../../common/components/actions-renderer.component';
import { MobileActionsRendererComponent } from '../../common/components/mobile-actions-renderer.component';
import { CommonEngine } from '@angular/ssr';
import { CommonModule, DatePipe } from '@angular/common';
import { AgGridAngular } from 'ag-grid-angular';
import { FormsModule } from '@angular/forms';
import { HolydayCallenderService } from '../services/HolydayCallender.service';
import { ToastrService } from 'ngx-toastr';
import { LoaderService } from '../../common/services/loader.service';
import { AuditFieldsService } from '../../common/services/auditfields.service';
import { DeleteConfirmationComponent } from '../../common/components/delete.compunent';
import { CreateHolydaycallenderComponent } from './create-holydaycallender.component';

ModuleRegistry.registerModules([AllCommunityModule]);

@Component({
  selector: 'app-holydaycallender-list',
  standalone: true,
  imports: [CommonModule, AgGridAngular, DatePipe, FormsModule, DeleteConfirmationComponent,CreateHolydaycallenderComponent],
  templateUrl: './holydaycallender-list.component.html',
  styleUrl: './holydaycallender-list.component.css'
})
export class HolydaycallenderListComponent {

  today = new Date();
  // Grid API
  private gridApi!: GridApi;

  // Responsive state
  isMobile: boolean = false;

  showDeletePopup = false;

  selectedDeleteItem: HolidayCallender | null = null;

  rowData: HolidayCallender[] = [];


  // Desktop Columns (7-8 columns)
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
      field: 'FestivalName',
      headerName: 'Festival Name',
      width: 180,
      filter: 'agTextColumnFilter',
      sortable: true,
      cellRenderer: this.nameRenderer.bind(this)
    },
    {
      field: 'HolidayDate',
      headerName: 'Holiday Date',
      width: 120,
      filter: 'agTextColumnFilter',
      sortable: true,
      cellClass: 'text-center'
    },
    {
      field: 'Year',
      headerName: 'Year',
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
        onEditClick: (data: any) => this.requestRoleProcess(data),
        onDeleteClick: (data: any) => this.deleteHoliday(data)
      },
      cellClass: 'text-center'
    }
  ];

  mobileColumnDefs: ColDef[] = [
    {
      field: 'FestivalName',
      headerName: 'Name',
      width: 180,
      cellRenderer: this.mobileNameRenderer.bind(this)
    },
    {
      field: 'HolidayDate',
      headerName: 'Date',
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
        onEditClick: (data: any) => this.requestRoleProcess(data)
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

  showsidebar: boolean = false;
  selectedHolidayCallender: HolidayCallender | null = null;

  constructor(
    private holidaycallenderService: HolydayCallenderService,
    private toastr: ToastrService,
    private loader: LoaderService,
    private audit: AuditFieldsService
  ) { }

  ngOnInit(): void {
    this.checkScreenSize();
    this.setupResponsiveColumns();
    this.loadHolydayCallender();
    window.addEventListener('resize', this.onResize.bind(this));
  }

  ngOnDestroy(): void {
    window.removeEventListener('resize', this.onResize.bind(this));
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
  onGridReady(params: GridReadyEvent): void {
    this.gridApi = params.api;
    setTimeout(() => {
      this.gridApi.sizeColumnsToFit();
    }, 300);
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


  loadHolydayCallender(): void {
    this.loader.show();

    this.holidaycallenderService.getHolydaysListAsync().subscribe({
      next: (holyday: HolidayCallender[]) => {
        this.rowData = holyday;
        this.loader.hide();
        if (this.gridApi) {
          setTimeout(() => {
            this.gridApi.sizeColumnsToFit();
          }, 100);
        }
      },
      error: (error) => {
        console.error('Error loading holiday:', error);
        this.loader.hide();

        this.toastr.error('Failed to load holiday', 'Error');
      }
    });
  }

  refreshData(): void {
    this.loadHolydayCallender();
  }

  deleteHoliday(holiday: HolidayCallender): void {
    this.selectedDeleteItem = holiday;
    this.showDeletePopup = true;
  }

  openAddEditholiday(): void {
    this.selectedHolidayCallender = null;
    this.showsidebar = true;
  }

  onCloseSidebar():void{
    this.selectedHolidayCallender=null;
    this.showsidebar=false;
  }

  closepopup(): void {
    this.showDeletePopup = false;
    this.selectedDeleteItem = null;
  }
  requestRoleProcess(holyday: HolidayCallender): void {
    this.showsidebar = true
    this.selectedHolidayCallender = holyday
  }

  getSelectedRowsCount(): number {
    return this.gridApi?.getSelectedRows()?.length || 0;
  }

  getTotalRowsCount(): number {
    return this.rowData.length;
  }

  getActiveHolydayCount(): number {
    return this.rowData.filter(holiday => holiday.IsActive).length;
  }

  getInactiveHolydayCount(): number {
    return this.rowData.filter(holiday => !holiday.IsActive).length;
  }


  deleteHolidayCallender() {
    if (!this.selectedDeleteItem) {
      console.error("No item selected for delete");
      return;
    }

    this.holidaycallenderService.deleteHolydayCallender(this.selectedDeleteItem.Id)
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

  onSaveHolidaycallender(holiday: HolidayCallender): void {
    this.loader.show();
    var _holiday = this.audit.appendAuditFields(holiday);
    console.log("we have receved holiday data " + JSON.stringify(holiday));
    this.holidaycallenderService.insertOrUpdateHolidayCallender(_holiday).subscribe(
      reponse => {
        if (reponse) {
          this.toastr.success("holiday processed succeessfully");
          this.showsidebar = false;
          this.refreshData();
        }
      }, error => {
        this.toastr.error("something went wrong , please check and resubmit");
        this.showsidebar = true;
        this.loader.hide();
      });
  }
}
