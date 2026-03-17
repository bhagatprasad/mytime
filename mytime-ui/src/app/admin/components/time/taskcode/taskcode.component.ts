import { Component, HostListener, OnDestroy, OnInit } from '@angular/core';
import { Taskcode } from '../../../models/taskcode';
import { AllCommunityModule, ColDef, GridApi, GridOptions, GridReadyEvent, ICellRendererParams, ModuleRegistry, ValueFormatterParams } from 'ag-grid-community';
import { ActionsRendererComponent } from '../../../../common/components/actions-renderer.component';
import { MobileActionsRendererComponent } from '../../../../common/components/mobile-actions-renderer.component';
import { TaskcodeService } from '../../../services/taskcode.service';
import { LoaderService } from '../../../../common/services/loader.service';
import { ToastrService } from 'ngx-toastr';
import { AuditFieldsService } from '../../../../common/services/auditfields.service';
import { CommonModule } from '@angular/common';
import { DeleteConfirmationComponent } from '../../../../common/components/delete.compunent';
import { AgGridAngular } from 'ag-grid-angular';
import { CreateTaskcodeComponent } from './create-taskcode.component';
import { TaskItem } from '../../../models/taskitem';
import { forkJoin } from 'rxjs';
import { TaskitemService } from '../../../services/taskitem.service';

ModuleRegistry.registerModules([AllCommunityModule]);

@Component({
  selector: 'app-taskcode',
  standalone: true,
  imports: [CommonModule, DeleteConfirmationComponent, AgGridAngular, CreateTaskcodeComponent],
  templateUrl: './taskcode.component.html',
  styleUrl: './taskcode.component.css'
})
export class TaskcodeComponent implements OnInit, OnDestroy {

  today = new Date();


  taskcodes: Taskcode[] = [];


  showDeletePopup: boolean = false;
  selectedDeleteItem: Taskcode | null = null;

  showSidebar: boolean = false;

  selectedtaskcode: Taskcode | null = null;



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
      field: 'TaskCodeId',
      headerName: 'ID',
      width: 80,
      filter: 'agNumberColumnFilter',
      sortable: true,
      cellClass: 'text-center'
    },
    {
      field: 'Name',
      headerName: 'Taskcode Name',
      width: 160,
      filter: 'agTextColumnFilter',
      sortable: true,
      cellRenderer: this.nameRenderer.bind(this)
    },
    {
      field: 'Code',
      headerName: ' Code',
      width: 120,
      filter: 'agTextColumnFilter',
      sortable: true,
      cellClass: 'text-center'
    },
    {
      field: 'TaskItemId',
      headerName: 'Item Name',
      width: 120,
      filter: 'agTextColumnFilter',
      sortable: true,
      cellClass: 'text-center',
      valueGetter: (params: any) => {
        const item = this.taskitems.find(x => x.TaskItemId === params.data.TaskItemId);
        return item ? item.Name : '';
      }
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
      field: 'IsActive',
      headerName: 'Status',
      width: 100,
      filter: 'agTextColumnFilter',
      sortable: true,
      cellRenderer: this.statusRenderer.bind(this),
      cellClass: this.statusCellClass.bind(this)
    },
    {
      field: 'Actions',
      headerName: 'Actions',
      width: 150,
      sortable: false,
      filter: false,
      cellRenderer: ActionsRendererComponent,
      cellRendererParams: {
        onEditClick: (data: any) => this.requesttaskcodeProcess(data),
        onDeleteClick: (data: any) => this.deletetaskcode(data)
      },
      cellClass: 'text-center'
    }
  ];

  mobileColumnDefs: ColDef[] = [
    {
      field: 'Name',
      headerName: 'City',
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
        onEditClick: (data: any) => this.requesttaskcodeProcess(data)
      },
      cellClass: 'text-center'
    }
  ];
  taskitems: TaskItem[] = [];
  constructor(private taskcodeservice: TaskcodeService,
    private loader: LoaderService,
    private toster: ToastrService,
    private audit: AuditFieldsService,private taskitemservice: TaskitemService) {

  }

  deletetaskcode(taskcode: Taskcode): void {
    this.showDeletePopup = true;
    this.selectedDeleteItem = taskcode;

  }
  requesttaskcodeProcess(taskcode: Taskcode): void {
    this.showSidebar = true;
    this.selectedtaskcode = taskcode;
  }

  loadTaskcodeData(): void {
    this.loader.show();
    forkJoin({
      taskitems: this.taskitemservice.GetTaskitemListAsync(),
      taskcode: this.taskcodeservice.getTaskcodeListAsync(),
    }).subscribe({
      next: ({ taskitems, taskcode }) => {
        this.taskitems = taskitems;
        this.taskcodes = taskcode;
        this.loader.hide();
        if (this.gridApi) {
          setTimeout(() => {
            this.gridApi.sizeColumnsToFit();
          }, 100);
        }
      }
    });
  }

  ngOnDestroy(): void {
    window.removeEventListener('resize', this.onResize.bind(this));
  }
  ngOnInit(): void {
    this.checkScreenSize();
    this.setupResponsiveColumns();
    this.loadTaskcodeData();
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
    return this.taskcodes.length;
  }

  getActiveTaskcodesCount(): number {
    return this.taskcodes.filter(c => c.IsActive).length;
  }

  getInactiveTaskcodesCount(): number {
    return this.taskcodes.filter(c => !c.IsActive).length;
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

    this.taskcodeservice.deleteTaskcodeAsync(this.selectedDeleteItem.TaskCodeId)
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
      });
  }
  refreshData() {
    this.loadTaskcodeData();
  }
  onCloseSidebar(): void {
    this.showSidebar = false;
    this.selectedtaskcode = null;
  }
  openAddEditTaskcode(): void {
    this.showSidebar = true;
    this.selectedtaskcode = null;
  }

  onSaveTaskcode(taskcode: any): void {
    this.loader.show();
    console.log(taskcode);
    const _taskocde = this.audit.appendAuditFields(taskcode);
    this.taskcodeservice.insertOrUpdateStateAsync(_taskocde).subscribe(reponse => {
      if (reponse) {
        this.toster.success("Taskcode processed succeessfully");
        this.showSidebar = false;
        this.refreshData();
      }
    }, error => {
      this.toster.error("something went wrong , please check and resubmit");
      this.showSidebar = true;
      this.loader.hide();
    });
  }

}
