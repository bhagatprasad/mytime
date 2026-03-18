import { CommonModule } from '@angular/common';
import { Component, HostListener, OnDestroy, OnInit } from '@angular/core';
import { AgGridAngular } from 'ag-grid-angular';
import {
  AllCommunityModule,
  ColDef,
  GridApi,
  GridOptions,
  GridReadyEvent,
  ICellRendererParams,
  ModuleRegistry,
  ValueFormatterParams,
} from 'ag-grid-community';
import { LeaveTypeService } from '../../services/leavetype.service';
import { LeaveType } from '../../models/leave-type.model';
import { MobileActionsRendererComponent } from '../../../common/components/mobile-actions-renderer.component';
import { ToastrService } from 'ngx-toastr';
import { LoaderService } from '../../../common/services/loader.service';
import { AuditFieldsService } from '../../../common/services/auditfields.service';
import { ActionsRendererComponent } from '../../../common/components/actions-renderer.component';
ModuleRegistry.registerModules([AllCommunityModule]);
@Component({
  selector: 'app-leavetype-list',
  standalone: true,
  imports: [CommonModule, AgGridAngular],
  templateUrl: './leavetype-list.component.html',
  styleUrl: './leavetype-list.component.css',
})
export class LeavetypeListComponent implements OnInit, OnDestroy {
  deleteLeaveType(leavetype: LeaveType): void {}
  requestLeaveTypeProcess(leavetype: LeaveType): void {}
  leavetype: LeaveType[] = [];

  today = new Date();
  // Grid API
  private gridApi!: GridApi;
  constructor(
    private leavetypeService: LeaveTypeService,
    private toastr: ToastrService,
    private loader: LoaderService,
    private audit: AuditFieldsService,
  ) {}

  ngOnInit(): void {
    this.loadLeaveTypeDetails();
    this.checkScreenSize();
    this.setupResponsiveColumns();

    window.addEventListener('resize', this.onResize.bind(this));
  }
  ngOnDestroy(): void {
    window.removeEventListener('resize', this.onResize.bind(this));
  }

  loadLeaveTypeDetails(): void {
    this.loader.show();
    this.leavetypeService.GetLeaveTypeListAsync().subscribe({
      next: (leavetype: LeaveType[]) => {
        console.log('Leave type Details:', leavetype);
        this.leavetype = leavetype;
        this.loader.hide();
        if (this.gridApi) {
          setTimeout(() => {
            this.gridApi.sizeColumnsToFit();
          }, 100);
        }
      },
      error: (error) => {
        console.error('Error fetching LeaveType Details', error);
        this.loader.hide();
        this.toastr.error('Failed to load leavetype', 'Error');
      },
    });
  }

  getTotalRowsCount(): number {
    return this.leavetype.length;
  }
  openAddEditLeaveType() {}
  columnDefs: ColDef[] = [];
  defaultColDef: ColDef = {
    flex: 1,
    minWidth: 100,
    filter: true,
    resizable: true,
    sortable: true,
    floatingFilter: false,
  };
  gridOptions: GridOptions = {
    pagination: true,
    paginationPageSize: 10,
    paginationPageSizeSelector: [10, 20, 40, 100],
    rowSelection: 'single',
    animateRows: true,
    enableCellTextSelection: true,
    suppressRowClickSelection: false,
    domLayout: 'autoHeight',
  };
  onGridReady(params: GridReadyEvent): void {
    this.gridApi = params.api;
    setTimeout(() => {
      this.gridApi.sizeColumnsToFit();
    }, 300);
  }
  isMobile: boolean = false;
  desktopColumnDefs: ColDef[] = [
    {
      field: 'Id',
      headerName: 'LeaveType ID',
      width: 80,
      filter: 'agNumberColumnFilter',
      sortable: true,
      cellClass: 'text-left',
    },
    {
      field: 'Name',
      headerName: 'LeaveType Name',
      width: 120,
      filter: 'agTextColumnFilter',
      sortable: true,
      cellRenderer: this.nameRenderer.bind(this),
    },
    {
      field: 'MaxDaysPerYear',
      headerName: 'MaxDays_perYr',
      width: 80,
      filter: 'agNumberColumnFilter',
      sortable: true,
      cellClass: 'text-left',
    },
    {
      field: 'Description',
      headerName: 'Description',
      width: 120,
      filter: 'agNumberColumnFilter',
      sortable: true,
      cellClass: 'text-left',
    },
    {
      field: 'CreatedBy',
      headerName: 'Created By',
      width: 120,
      filter: 'agNumberColumnFilter',
      sortable: true,
      cellClass: 'text-center',
    },
    {
      field: 'CreatedOn',
      headerName: 'Created Date',
      width: 120,
      filter: 'agDateColumnFilter',
      sortable: true,
      valueFormatter: this.dateFormatter.bind(this),
      cellClass: 'text-center',
    },
    {
      field: 'ModifiedBy',
      headerName: 'Modified By',
      width: 120,
      filter: 'agNumberColumnFilter',
      sortable: true,
      cellClass: 'text-center',
    },
    {
      field: 'ModifiedOn',
      headerName: 'Last Modified',
      width: 120,
      filter: 'agDateColumnFilter',
      sortable: true,
      valueFormatter: this.dateFormatter.bind(this),
      cellClass: 'text-center',
    },
    {
      field: 'Actions',
      headerName: 'Actions',
      width: 150,
      sortable: false,
      filter: false,
      cellRenderer: ActionsRendererComponent,
      cellRendererParams: {
        onEditClick: (data: any) => this.requestLeaveTypeProcess(data),
        onDeleteClick: (data: any) => this.deleteLeaveType(data),
      },
      cellClass: 'text-left',
    },
  ];
  mobileColumnDefs: ColDef[] = [
    {
      field: 'Name',
      headerName: 'LeaveType_Name',
      width: 180,
      cellRenderer: this.mobileNameRenderer.bind(this),
    },
    {
      field: 'MaxDaysPerYear',
      headerName: 'MaxDays_perYr',
      width: 80,
      cellClass: 'text-center',
    },
    {
      field: 'Actions',
      headerName: '',
      width: 80,
      sortable: false,
      filter: false,
      cellRenderer: MobileActionsRendererComponent,
      cellRendererParams: {
        onEditClick: (data: any) => this.requestLeaveTypeProcess(data),
      },
      cellClass: 'text-center',
    },
  ];
  nameRenderer(params: ICellRendererParams): string {
    return `
        <div class="leavetype-name-cell">
          <strong>${params.value}</strong>
          <div class="text-muted small">Code: ${params.data.Code}</div>
        </div>
      `;
  }
  mobileNameRenderer(params: ICellRendererParams): string {
    return `
      <div class="mobile-leavetype-cell">
        <strong>${params.value}</strong>
        <div class="text-muted small">ID: ${params.data.Id}</div>
      </div>
    `;
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
  @HostListener('window:resize', ['$event'])
  onResize(event: any): void {
    this.checkScreenSize();
  }
  getActiveLeaveTypeCount(): number {
    return this.leavetype.filter((leavetype) => leavetype.IsActive).length;
  }
  getInactiveLeaveTypeCount(): number {
    return this.leavetype.filter((leavetype) => !leavetype.IsActive).length;
  }
  refreshData(): void {
    this.loadLeaveTypeDetails();
  }
  dateFormatter(params: ValueFormatterParams): string {
    if (!params.value) return 'N/A';

    const date = new Date(params.value);
    if (isNaN(date.getTime())) return 'Invalid Date';

    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  }
}
