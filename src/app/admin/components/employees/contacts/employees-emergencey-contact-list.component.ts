import { CommonModule } from '@angular/common';
import { Component, HostListener, Input, OnDestroy, OnInit } from '@angular/core';
import { AgGridAngular } from 'ag-grid-angular';
import { AllCommunityModule, ColDef, GridApi, GridOptions, GridReadyEvent, ICellRenderer, ICellRendererParams, ModuleRegistry } from 'ag-grid-community';
import { EmployeeEmergencyContact } from '../../../models/employee_emergency_contact';
import { ActionsRendererComponent } from '../../../../common/components/actions-renderer.component';
import { MobileActionsRendererComponent } from '../../../../common/components/mobile-actions-renderer.component';
import { LoaderService } from '../../../../common/services/loader.service';
import { ToastrService } from 'ngx-toastr';
import { AuditFieldsService } from '../../../../common/services/auditfields.service';
import { EmployeeEmergencyContactService } from '../../../services/employee_contact.service';
import { EmployeesEmergencyContactAddComponent } from './employees-emergencey-contact-add.component';

ModuleRegistry.registerModules([AllCommunityModule]);


@Component({
  selector: 'app-employees-emergencey-contact-list',
  standalone: true,
  imports: [CommonModule, AgGridAngular, EmployeesEmergencyContactAddComponent],
  templateUrl: './employees-emergencey-contact-list.component.html',
  styleUrl: './employees-emergencey-contact-list.component.css'
})
export class EmployeesEmergenceyContactListComponent implements OnInit, OnDestroy {

  @Input() employeeId: number | null = null;

  private emergenceyContactsGridApi!: GridApi;

  isMobile: boolean = false;

  contacts: EmployeeEmergencyContact[] = [];

  showEmergencyContactForm = false;

  selectedEmergencyContact: EmployeeEmergencyContact | null = null;


  desktopColumnDefs: ColDef[] = [
    {
      field: 'Name',
      headerName: 'Name',
      width: 150,
      filter: 'agTextColumnFilter',
      sortable: true
    },
    {
      field: 'Relation',
      headerName: 'Relation',
      width: 150,
      filter: 'agTextColumnFilter',
      sortable: true
    },
    {
      field: 'Phone',
      headerName: 'Phone',
      width: 100,
      filter: 'agNumberColumnFilter',
      sortable: true,
      cellClass: 'text-center'
    },
    {
      field: 'Email',
      headerName: 'Email',
      width: 100,
      filter: 'agNumberColumnFilter',
      sortable: true,
      cellClass: 'text-center'
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
      field: 'Actions',
      headerName: 'Actions',
      width: 150,
      sortable: false,
      filter: false,
      cellRenderer: ActionsRendererComponent,
      cellRendererParams: {
        onEditClick: (data: any) => this.openEditEmergencyContactForm(data),
        onDeleteClick: (data: any) => this.deleteEmergencyContact(data)
      },
      cellClass: 'text-center'
    }
  ];

  mobileColumnDefs: ColDef[] = [
    {
      field: 'Name',
      headerName: 'Name',
      width: 120
    },
    {
      field: 'Contact',
      headerName: 'Phone',
      width: 120,
      cellRenderer: this.contactInfoRender.bind(this),
    },
    {
      field: 'Actions',
      headerName: '',
      width: 80,
      sortable: false,
      filter: false,
      cellRenderer: MobileActionsRendererComponent,
      cellRendererParams: {
        onEditClick: (data: any) => this.openEditEmergencyContactForm(data),
        onDeleteClick: (data: any) => this.deleteEmergencyContact(data)
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

  contactGridOptions: GridOptions = {
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
    private contactsService: EmployeeEmergencyContactService,
    private loader: LoaderService,
    private notify: ToastrService,
    private audit: AuditFieldsService) { }

  ngOnDestroy(): void {
    window.removeEventListener('resize', this.onResize.bind(this));
  }
  ngOnInit(): void {
    this.checkScreenSize();
    this.setupResponsiveColumns();
    this.loadEmploymentData();
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
      this.contactGridOptions.domLayout = 'autoHeight';
    } else {
      this.columnDefs = [...this.desktopColumnDefs];
      this.contactGridOptions.domLayout = 'normal';
    }

    if (this.emergenceyContactsGridApi) {
      this.refreshGridColumns();
    }
  }

  private refreshGridColumns(): void {
    if (!this.emergenceyContactsGridApi) return;
    setTimeout(() => {
      this.emergenceyContactsGridApi.refreshHeader();
      this.emergenceyContactsGridApi.sizeColumnsToFit();
    }, 100);
  }

  loadEmploymentData(): void {
    if (!this.employeeId) return;

    this.loader.show();
    this.contactsService.getEmergencyContactsByEmployeeAsync(this.employeeId).subscribe({
      next: (employeeEmergencyContacts: EmployeeEmergencyContact[]) => {
        this.contacts = employeeEmergencyContacts;
        this.loader.hide();
        if (this.emergenceyContactsGridApi) {
          setTimeout(() => {
            this.emergenceyContactsGridApi.sizeColumnsToFit();
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
    this.emergenceyContactsGridApi = params.api;
    setTimeout(() => {
      this.emergenceyContactsGridApi.sizeColumnsToFit();
    }, 300);
  }

  @HostListener('window:resize')
  onResize(): void {
    this.checkScreenSize();
  }

  refreshData(): void {
    this.loadEmploymentData();
  }

  onSaveEmergencyContact(employeeEmergencyContact: EmployeeEmergencyContact): void {
    console.log(employeeEmergencyContact);
    this.loader.show();
    if (!employeeEmergencyContact.EmployeeEmergencyContactId && this.employeeId) {
      employeeEmergencyContact.EmployeeId = this.employeeId;
    }

    const _contact = this.audit.appendAuditFields(employeeEmergencyContact);
    this.contactsService.insertOrUpdateEmployeeEmergencyContactAsync(_contact).subscribe({
      next: (response) => {
        if (response) {
          this.notify.success('Education saved successfully');
          this.showEmergencyContactForm = false;
          this.selectedEmergencyContact = null;
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
  openAddEmergencyContactForm(): void {
    this.selectedEmergencyContact = null;
    this.showEmergencyContactForm = true;
  }
  onCloseEmergencyContactForm(): void {
    this.selectedEmergencyContact = null;
    this.showEmergencyContactForm = false;
  }
  openEditEmergencyContactForm(contact: EmployeeEmergencyContact): void {
    this.selectedEmergencyContact = contact;
    this.showEmergencyContactForm = true;
  }
  deleteEmergencyContact(contact: EmployeeEmergencyContact): void {

  }
  contactInfoRender(param: ICellRendererParams): string {
    const data = param.data as EmployeeEmergencyContact;

    if (!data) return '';

    const contactItems = [];

    if (data.Phone) {
      contactItems.push(`<span class="icon">📞</span> ${data.Phone}`);
    }

    if (data.Email) {
      contactItems.push(`<span class="icon">✉️</span> ${data.Email}`);
    }

    if (data.Relation) {
      contactItems.push(`<span class="icon">👤</span> ${data.Relation}`);
    }
    return `<span class="contact-info">${contactItems.join('<br>')}</span>`;
  }
  getTotalRowsCount(): number {
    return this.contacts.length;
  }

  getActiveContactsCount(): number {
    return this.contacts.filter(x => x.IsActive == true).length;
  }
}
