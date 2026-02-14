import { CommonModule } from '@angular/common';
import { Component, HostListener, Input, OnDestroy, OnInit } from '@angular/core';
import { AgGridAngular } from 'ag-grid-angular';
import { AllCommunityModule, ColDef, GridApi, GridOptions, GridReadyEvent, ICellRendererParams, ModuleRegistry } from 'ag-grid-community';
import { EmployeesEmployementAddComponent } from './employees-employement-add.component';
import { EmployeeEmployment } from '../../../models/employee_employment';
import { ActionsRendererComponent } from '../../../../common/components/actions-renderer.component';
import { MobileActionsRendererComponent } from '../../../../common/components/mobile-actions-renderer.component';
import { EmployeeEmploymentService } from '../../../services/employee_employeement.service';
import { LoaderService } from '../../../../common/services/loader.service';
import { ToastrService } from 'ngx-toastr';
import { AuditFieldsService } from '../../../../common/services/auditfields.service';

ModuleRegistry.registerModules([AllCommunityModule]);

@Component({
  selector: 'app-employees-employement-list',
  standalone: true,
  imports: [CommonModule, AgGridAngular, EmployeesEmployementAddComponent],
  templateUrl: './employees-employement-list.component.html',
  styleUrl: './employees-employement-list.component.css'
})
export class EmployeesEmployementListComponent implements OnInit, OnDestroy {


  @Input() employeeId: number | null = null;

  private employementGridApi!: GridApi;

  isMobile: boolean = false;

  employeements: EmployeeEmployment[] = [];

  showEmployementForm = false;

  selectedEmployement: EmployeeEmployment | null = null;

  desktopColumnDefs: ColDef[] = [
    {
      field: 'CompanyName',
      headerName: 'CompanyName',
      width: 150,
      filter: 'agTextColumnFilter',
      sortable: true
    },
    {
      field: 'Designation',
      headerName: 'Designation',
      width: 150,
      filter: 'agTextColumnFilter',
      sortable: true
    },
    {
      field: 'Address',
      headerName: 'Address',
      width: 100,
      filter: 'agNumberColumnFilter',
      sortable: true,
      cellClass: 'text-center'
    },
    {
      field: 'StartedOn',
      headerName: 'Duration',
      width: 150,
      sortable: false,
      filter: false,
      cellRenderer: this.durationRenderer.bind(this),
    },
    {
      field: 'Actions',
      headerName: 'Actions',
      width: 150,
      sortable: false,
      filter: false,
      cellRenderer: ActionsRendererComponent,
      cellRendererParams: {
        onEditClick: (data: any) => this.openEditEmployementForm(data),
        onDeleteClick: (data: any) => this.deleteEmployement(data)
      },
      cellClass: 'text-center'
    }
  ];

  mobileColumnDefs: ColDef[] = [
    {
      field: 'CompanyName',
      headerName: 'CompanyName',
      width: 120
    },
    {
      field: 'Designation',
      headerName: 'Designation',
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
        onEditClick: (data: any) => this.openEditEmployementForm(data),
        onDeleteClick: (data: any) => this.deleteEmployement(data)
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

  employeementGridOptions: GridOptions = {
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
    private employeementService: EmployeeEmploymentService,
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
    this.loadEmploymentData();
    window.addEventListener('resize', this.onResize.bind(this));
  }

  openEditEmployementForm(employeement: EmployeeEmployment): void {
    this.selectedEmployement = employeement;
    this.showEmployementForm = true;
  }
  deleteEmployement(employeement: EmployeeEmployment): void {

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
      this.employeementGridOptions.domLayout = 'autoHeight';
    } else {
      this.columnDefs = [...this.desktopColumnDefs];
      this.employeementGridOptions.domLayout = 'normal';
    }

    if (this.employementGridApi) {
      this.refreshGridColumns();
    }
  }

  private refreshGridColumns(): void {
    if (!this.employementGridApi) return;
    setTimeout(() => {
      // this.employementGridApi.setColumnDefs(this.columnDefs);
      this.employementGridApi.refreshHeader();
      this.employementGridApi.sizeColumnsToFit();
    }, 100);
  }

  loadEmploymentData(): void {
    if (!this.employeeId) return;

    this.loader.show();
    this.employeementService.getEmploymentsByEmployeeAsync(this.employeeId).subscribe({
      next: (employeements: EmployeeEmployment[]) => {
        this.employeements = employeements;
        this.loader.hide();
        if (this.employementGridApi) {
          setTimeout(() => {
            this.employementGridApi.sizeColumnsToFit();
          }, 100);
        }
      },
      error: (error) => {
        console.error('Error loading employements:', error);
        this.loader.hide();
        this.notify.error('Failed to load employements', 'Error');
      }
    });
  }

  onGridReady(params: GridReadyEvent): void {
    this.employementGridApi = params.api;
    setTimeout(() => {
      this.employementGridApi.sizeColumnsToFit();
    }, 300);
  }

  @HostListener('window:resize')
  onResize(): void {
    this.checkScreenSize();
  }

  refreshData(): void {
    this.loadEmploymentData();
  }

  onSaveEmployeement(employeement: EmployeeEmployment): void {
    console.log(employeement);
    this.loader.show();
    if (!employeement.EmployeeEmploymentId && this.employeeId) {
      employeement.EmployeeId = this.employeeId;
    }

    const _employeement = this.audit.appendAuditFields(employeement);
    this.employeementService.insertOrUpdateEmployementAsync(_employeement).subscribe({
      next: (response) => {
        if (response) {
          this.notify.success('Education saved successfully');
          this.showEmployementForm = false;
          this.selectedEmployement = null;
          this.loadEmploymentData();
        }
      },
      error: (error) => {
        console.error('Error saving education:', error);
        this.notify.error('Failed to save education');
        this.loader.hide();
      }
    });
  }
  onCloseEmployeementForm(): void {
    this.selectedEmployement = null;
    this.showEmployementForm = false;
  }
  openAddEmployeementForm(): void {
    this.selectedEmployement = null;
    this.showEmployementForm = true;
  }

  getActiveEmployeementsCount(): number {
    return this.employeements.filter(x => x.IsActive == true).length;
  }
  getTotalRowsCount(): number {
    return this.employeements.length;
  }

  durationRenderer(params: ICellRendererParams): string {
    const startedOn = params.data?.StartedOn;
    const endedOn = params.data?.EndedOn;
    const formatDate = (dateStr: string | null): string => {
      if (!dateStr) return '';

      try {
        const date = new Date(dateStr);
        if (isNaN(date.getTime())) return '';

        const month = (date.getMonth() + 1).toString().padStart(2, '0');
        const day = date.getDate().toString().padStart(2, '0');
        const year = date.getFullYear();

        return `${month}-${day}-${year}`;
      } catch (error) {
        console.error('Error formatting date:', error);
        return '';
      }
    };

    const startFormatted = formatDate(startedOn);
    const endFormatted = formatDate(endedOn);
    if (!startFormatted && !endFormatted) {
      return '<span class="text-muted">No dates</span>';
    }
    return `
    <div class="d-flex align-items-center gap-1">
      <span class="fw-medium">${startFormatted || '??-??-????'}</span>
      <span class="text-muted mx-1">—</span>
      <span class="fw-medium">${endFormatted || 'Present'}</span>
    </div>
  `;
  }
}