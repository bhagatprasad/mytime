import { CommonModule } from '@angular/common';
import { Component, HostListener, OnDestroy, OnInit, Input } from '@angular/core';
import { AgGridAngular } from 'ag-grid-angular';
import {
  AllCommunityModule,
  ColDef,
  GridApi,
  GridOptions,
  GridReadyEvent,
  ICellRendererParams,
  ModuleRegistry,
  ValueFormatterParams
} from 'ag-grid-community';
import { EmployeeEducation } from '../../../models/employee_education';
import { ActionsRendererComponent } from '../../../../common/components/actions-renderer.component';
import { MobileActionsRendererComponent } from '../../../../common/components/mobile-actions-renderer.component';
import { EmployeeEducationService } from '../../../services/employee_education.service';
import { LoaderService } from '../../../../common/services/loader.service';
import { ToastrService } from 'ngx-toastr';
import { EmployeesEducationAddComponent } from './employees-education-add.component';
import { AuditFieldsService } from '../../../../common/services/auditfields.service';

ModuleRegistry.registerModules([AllCommunityModule]);

@Component({
  selector: 'app-employees-education-list',
  standalone: true,
  imports: [CommonModule, AgGridAngular, EmployeesEducationAddComponent],
  templateUrl: './employees-education-list.component.html',
  styleUrls: ['./employees-education-list.component.css']
})
export class EmployeesEducationListComponent implements OnInit, OnDestroy {
  @Input() employeeId: number | null = null;

  private educationGridApi!: GridApi;
  isMobile: boolean = false;
  educations: EmployeeEducation[] = [];

  // Form visibility
  showEducationForm = false;
  selectedEducation: EmployeeEducation | null = null;

  desktopColumnDefs: ColDef[] = [
    {
      field: 'Degree',
      headerName: 'Degree',
      width: 150,
      filter: 'agTextColumnFilter',
      sortable: true
    },
    {
      field: 'FeildOfStudy',
      headerName: 'Field Of Study',
      width: 150,
      filter: 'agTextColumnFilter',
      sortable: true
    },
    {
      field: 'Institution',
      headerName: 'Institution',
      width: 150,
      filter: 'agTextColumnFilter',
      sortable: true
    },
    {
      field: 'Year',
      headerName: 'Year',
      width: 100,
      filter: 'agNumberColumnFilter',
      sortable: true,
      cellClass: 'text-center'
    },
    {
      field: 'PercentageMarks',
      headerName: 'Percentage',
      width: 120,
      filter: 'agNumberColumnFilter',
      sortable: true,
      cellClass: 'text-center',
      valueFormatter: this.percentageFormatter.bind(this)
    },
    {
      field: 'Actions',
      headerName: 'Actions',
      width: 150,
      sortable: false,
      filter: false,
      cellRenderer: ActionsRendererComponent,
      cellRendererParams: {
        onEditClick: (data: any) => this.openEditEducationForm(data),
        onDeleteClick: (data: any) => this.deleteEducation(data)
      },
      cellClass: 'text-center'
    }
  ];

  mobileColumnDefs: ColDef[] = [
    {
      field: 'Degree',
      headerName: 'Degree',
      width: 180,
      cellRenderer: this.mobileDegreeRenderer.bind(this)
    },
    {
      field: 'Institution',
      headerName: 'Institution',
      width: 120
    },
    {
      field: 'Actions',
      headerName: '',
      width: 80,
      sortable: false,
      filter: false,
      cellRenderer: MobileActionsRendererComponent,
      cellRendererParams: {
        onEditClick: (data: any) => this.openEditEducationForm(data),
        onDeleteClick: (data: any) => this.deleteEducation(data)
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

  educationGridOptions: GridOptions = {
    pagination: true,
    paginationPageSize: 10,
    paginationPageSizeSelector: [10, 20, 50, 100],
    rowSelection: 'single',
    animateRows: true,
    enableCellTextSelection: true,
    suppressRowClickSelection: false,
    domLayout: 'autoHeight'
  };

  constructor(
    private employeeEducationService: EmployeeEducationService,
    private loader: LoaderService,
    private notify: ToastrService,
    private audit: AuditFieldsService
  ) { }

  ngOnDestroy(): void {
    window.removeEventListener('resize', this.onResize.bind(this));
  }

  ngOnInit(): void {
    this.checkScreenSize();
    this.setupResponsiveColumns();
    this.loadEducationData();
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
      this.educationGridOptions.domLayout = 'autoHeight';
    } else {
      this.columnDefs = [...this.desktopColumnDefs];
      this.educationGridOptions.domLayout = 'normal';
    }

    if (this.educationGridApi) {
      this.refreshGridColumns();
    }
  }

  private refreshGridColumns(): void {
    if (!this.educationGridApi) return;
    setTimeout(() => {
      // this.educationGridApi.setColumnDefs(this.columnDefs);
      this.educationGridApi.refreshHeader();
      this.educationGridApi.sizeColumnsToFit();
    }, 100);
  }

  loadEducationData(): void {
    if (!this.employeeId) return;

    this.loader.show();
    this.employeeEducationService.getEmployeeEducationsListAsync(this.employeeId).subscribe({
      next: (employeeEducations: EmployeeEducation[]) => {
        this.educations = employeeEducations;
        this.loader.hide();
        if (this.educationGridApi) {
          setTimeout(() => {
            this.educationGridApi.sizeColumnsToFit();
          }, 100);
        }
      },
      error: (error) => {
        console.error('Error loading educations:', error);
        this.loader.hide();
        this.notify.error('Failed to load educations', 'Error');
      }
    });
  }

  onGridReady(params: GridReadyEvent): void {
    this.educationGridApi = params.api;
    setTimeout(() => {
      this.educationGridApi.sizeColumnsToFit();
    }, 300);
  }

  @HostListener('window:resize')
  onResize(): void {
    this.checkScreenSize();
  }

  refreshData(): void {
    this.loadEducationData();
  }

  openAddEducationForm(): void {
    this.selectedEducation = null;
    this.showEducationForm = true;
  }

  openEditEducationForm(education: EmployeeEducation): void {
    this.selectedEducation = education;
    this.showEducationForm = true;
  }

  deleteEducation(education: EmployeeEducation): void {
    if (confirm('Are you sure you want to delete this education record?')) {
      this.loader.show();
      // this.employeeEducationService.deleteEmployeeEducation(education.EmployeeEducationId).subscribe({
      //   next: () => {
      //     this.notify.success('Education record deleted successfully');
      //     this.loadEducationData();
      //   },
      //   error: (error) => {
      //     console.error('Error deleting education:', error);
      //     this.notify.error('Failed to delete education record');
      //     this.loader.hide();
      //   }
      // });
    }
  }

  onCloseEducationForm(): void {
    this.showEducationForm = false;
    this.selectedEducation = null;
  }
  prepareEmployeeEducationPayload(data: any): EmployeeEducation {
    return {
      ...data,
      PercentageMarks: data.PercentageMarks?.toString() || null
    };
  }

  onSaveEducation(education: EmployeeEducation): void {
    this.loader.show();

    // Set employee ID if it's a new education
    if (!education.EmployeeEducationId && this.employeeId) {
      education.EmployeeId = this.employeeId;
    }

    const _education = this.prepareEmployeeEducationPayload(this.audit.appendAuditFields(education));


    this.employeeEducationService.insertOrUpdateEmployeeEducationAsync(_education).subscribe({
      next: (response) => {
        if (response) {
          this.notify.success('Education saved successfully');
          this.showEducationForm = false;
          this.selectedEducation = null;
          this.loadEducationData();
        }
      },
      error: (error) => {
        console.error('Error saving education:', error);
        this.notify.error('Failed to save education');
        this.loader.hide();
      }
    });
  }

  getTotalRowsCount(): number {
    return this.educations.length;
  }

  getActiveEducationsCount(): number {
    return this.educations.filter(e => e.IsActive).length;
  }

  // ========== CELL RENDERERS ==========
  mobileDegreeRenderer(params: ICellRendererParams): string {
    return `
      <div class="mobile-education-cell">
        <strong>${params.value}</strong>
        <div class="text-muted small">${params.data.FieldOfStudy || ''}</div>
      </div>
    `;
  }

  statusCellClass(params: any): string {
    return params.value ? 'status-active' : 'status-inactive';
  }

  percentageFormatter(params: ValueFormatterParams): string {
    return params.value ? `${params.value}%` : 'N/A';
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
}