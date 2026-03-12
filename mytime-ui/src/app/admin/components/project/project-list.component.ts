import { CommonModule, DatePipe } from '@angular/common';
import { Component, HostListener, OnDestroy, OnInit } from '@angular/core';
import { AgGridAngular } from 'ag-grid-angular';
import {
  ColDef,
  GridApi,
  GridReadyEvent,
  GridOptions,
  ICellRendererParams,
  ValueFormatterParams,
  ModuleRegistry,
  AllCommunityModule,
} from 'ag-grid-community';
import { ProjectService } from '../../services/project_service';
import { Project } from '../../models/project';
import { ToastrService } from 'ngx-toastr';
import { LoaderService } from '../../../common/services/loader.service';
import { AuditFieldsService } from '../../../common/services/auditfields.service';
import { FormsModule } from '@angular/forms';
import { ActionsRendererComponent } from '../../../common/components/actions-renderer.component';
import { MobileActionsRendererComponent } from '../../../common/components/mobile-actions-renderer.component';
import { ProjectAddComponent } from './project-add.component';
import { DeleteConfirmationComponent } from '../../../common/components/delete.compunent';

ModuleRegistry.registerModules([AllCommunityModule]);

@Component({
  selector: 'app-project-list',
  standalone: true,
  imports: [
    CommonModule,
    AgGridAngular,
    DatePipe,
    FormsModule,
    ProjectAddComponent,
    DeleteConfirmationComponent,
  ],
  templateUrl: './project-list.component.html',
  styleUrl: './project-list.component.css',
})
export class ProjectListComponent implements OnInit, OnDestroy {
  projectDetails: Project[] = [];

  today = new Date();
  // Grid API
  private gridApi!: GridApi;

  // Responsive state
  isMobile: boolean = false;

  showSidebar: boolean = false;
  selectedProject: Project | null = null;

  showDeletePopup = false;

  selectedDeleteItem: Project | null = null;

  constructor(
    private projectservice: ProjectService,
    private toaster: ToastrService,
    private loader: LoaderService,
    private audit: AuditFieldsService,
  ) {}
  ngOnInit(): void {
    this.checkScreenSize();
    this.setupResponsiveColumns();
    window.addEventListener('resize', this.onResize.bind(this));
    this.loadProjectDetails();
  }

  loadProjectDetails(): void {
    this.loader.show();
    this.projectservice.getProjectListAsync().subscribe({
      next: (response: any) => {
        console.log('Project Details : ', response);
        console.log('Project length is : ', response.items.length);
        this.projectDetails = response.items;
        this.loader.hide();
        if (this.gridApi) {
          setTimeout(() => {
            this.gridApi.sizeColumnsToFit();
          }, 100);
        }
      },
      error: (error) => {
        console.error('Error fetching project details :', error);
        this.loader.hide();
        this.toaster.error('Failed to load projects', 'Error');
      },
    });
  }

  onGridReady(params: GridReadyEvent): void {
    this.gridApi = params.api;
    setTimeout(() => {
      this.gridApi.sizeColumnsToFit();
    }, 300);
  }

  ngOnDestroy(): void {
    window.removeEventListener('resize', this.onResize.bind(this));
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

  @HostListener('window:resize', ['$event'])
  onResize(event: any): void {
    this.checkScreenSize();
  }

  private refreshGridColumns(): void {
    if (!this.gridApi) return;
    const newColumnDefs = JSON.parse(JSON.stringify(this.columnDefs));
    setTimeout(() => {
      this.gridApi.refreshHeader();
      this.gridApi.sizeColumnsToFit();
    }, 100);
  }

  getSelectedRowsCount(): number {
    return this.gridApi?.getSelectedRows()?.length || 0;
  }

  desktopColumnDefs: ColDef[] = [
    {
      field: 'ProjectId',
      headerName: 'Project ID',
      width: 120,
      filter: 'agNumberColumnFilter',
      sortable: true,
      cellClass: 'text-left',
    },
    {
      field: 'Name',
      headerName: 'Project Name',
      width: 120,
      filter: 'agTextColumnFilter',
      sortable: true,
      cellRenderer: this.nameRenderer.bind(this),
    },

    {
      field: 'CreatedBy',
      headerName: 'Created By',
      width: 120,
      filter: 'agNumberColumnFilter',
      sortable: true,
      cellClass: 'text-left',
    },
    {
      field: 'CreatedOn',
      headerName: 'Created Date',
      width: 120,
      filter: 'agDateColumnFilter',
      sortable: true,
      valueFormatter: this.dateFormatter.bind(this),
      cellClass: 'text-left',
    },
    {
      field: 'ModifiedBy',
      headerName: 'Modified By',
      width: 120,
      filter: 'agNumberColumnFilter',
      sortable: true,
      cellClass: 'text-left',
    },
    {
      field: 'ModifiedOn',
      headerName: 'Last Modified',
      width: 120,
      filter: 'agDateColumnFilter',
      sortable: true,
      valueFormatter: this.dateFormatter.bind(this),
      cellClass: 'text-left',
    },
    {
      field: 'IsActive',
      headerName: 'Status',
      width: 120,
      filter: 'agTextColumnFilter',
      sortable: true,
      cellRenderer: this.statusRenderer.bind(this),
      cellClass: this.statusCellClass.bind(this),
    },
    {
      field: 'Actions',
      headerName: 'Actions',
      width: 150,
      sortable: false,
      filter: false,
      cellRenderer: ActionsRendererComponent,
      cellRendererParams: {
        onEditClick: (data: any) => this.requestProjectProcess(data),
        onDeleteClick: (data: any) => this.deleteProject(data),
      },
      cellClass: 'text-left',
    },
  ];

  mobileColumnDefs: ColDef[] = [
    {
      field: 'Name',
      headerName: 'Project Name',
      width: 180,
      cellRenderer: this.mobileNameRenderer.bind(this),
    },

    {
      field: 'Actions',
      headerName: 'Actions',
      width: 80,
      sortable: false,
      filter: false,
      cellRenderer: MobileActionsRendererComponent,
      cellRendererParams: {
        onEditClick: (data: any) => this.requestProjectProcess(data),
      },
      cellClass: 'text-left',
    },
  ];

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
    paginationPageSizeSelector: [20, 40, 60, 100],
    rowSelection: 'single',
    animateRows: true,
    enableCellTextSelection: true,
    suppressRowClickSelection: false,
    domLayout: 'autoHeight',
  };

  nameRenderer(params: ICellRendererParams): string {
    return `
      <div class="project-name-cell">
        <strong>${params.value}</strong>
        <div class="text-muted small">Code: ${params.data.Code}</div>
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

  statusCellClass(params: any): string {
    const isActive = params.value;
    return isActive ? 'status-active' : 'status-inactive';
  }

  mobileNameRenderer(params: ICellRendererParams): string {
    return `
      <div class="mobile-project-cell">
        <strong>${params.value}</strong>
        <div class="text-muted small">ID: ${params.data.Id}</div>
      </div>
    `;
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

  getTotalRowsCount(): number {
    return this.projectDetails.length;
  }

  getActiveProjectsCount(): number {
    return this.projectDetails.filter((project) => project.IsActive).length;
  }

  getInactiveProjectsCount(): number {
    return this.projectDetails.filter((project) => !project.IsActive).length;
  }
  openAddEditProject() {
    this.showSidebar = true;
    this.selectedProject = null;
  }

  requestProjectProcess(project: Project): void {
    this.selectedProject = project;
    this.showSidebar = true;
  }

  deleteProject(project: Project): void {
    this.selectedDeleteItem = project;
    this.showDeletePopup = true;
    console.log(JSON.stringify(project));
  }
  onSaveProject(project: Project): void {
    this.loader.show();
    var _project = this.audit.appendAuditFields(project);
    console.log('we have received project data ' + JSON.stringify(project));
    this.projectservice.saveProjectAsync(_project).subscribe(
      (response) => {
        if (response) {
          this.toaster.success('Project processed succeessfully');
          this.showSidebar = false;
          this.loader.hide();
          this.refreshData();
        }
      },
      (error) => {
        this.toaster.error('something went wrong , please check and resubmit');
        this.showSidebar = true;
        this.loader.hide();
      },
    );
  }

  onCloseSidebar(): void {
    this.showSidebar = false;
  }
  refreshData(): void {
    this.loadProjectDetails();
  }

  deleteproject() {
    if (!this.selectedDeleteItem) {
      console.error('No item selected for delete');
      return;
    }

    this.projectservice
      .deleteProjectAsync(this.selectedDeleteItem.ProjectId)
      .subscribe({
        next: (res) => {
          console.log('Delete success:', res);

          this.refreshData(); // reload grid data
          this.showDeletePopup = false;
          this.selectedDeleteItem = null;
        },
        error: (err) => {
          console.error('Delete failed:', err);
          // keep popup open OR close — your choice
          this.showDeletePopup = false;
        },
        complete: () => {
          alert('Delete request completed');
        },
      });
  }
  closePopup(): void {
    this.showDeletePopup = false;
    this.selectedDeleteItem = null;
  }
}
