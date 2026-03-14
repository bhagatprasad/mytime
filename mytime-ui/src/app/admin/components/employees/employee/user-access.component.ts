import { CommonModule } from "@angular/common";
import { Component, EventEmitter, Input, OnChanges, Output, SimpleChanges } from "@angular/core";
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from "@angular/forms";
import { RegisterUser } from "../../../models/register_user";
import { Role } from "../../../models/role";
import { Department } from "../../../models/department";
import { Designation } from "../../../models/designation";
import { Employee } from "../../../models/employee";
import { TogglePasswordDirective } from "../../../../common/directives/toggle-password.directive";

@Component({
    selector: 'app-user-access',
    standalone: true,
    imports: [CommonModule, ReactiveFormsModule, TogglePasswordDirective],
    templateUrl: './user-access.component.html',
    styleUrls: ['./user-access.component.css']
})
export class UserAccessComponent implements OnChanges {

    @Input() isVisible: boolean = false;
    @Input() registerUser: RegisterUser | null = null;
    @Input() roles: Role[] = [];
    @Input() departments: Department[] = [];
    @Input() designations: Designation[] = [];
    @Input() employee: Employee | null = null;

    @Output() saveUserAcess = new EventEmitter<RegisterUser>();
    @Output() close = new EventEmitter<void>();

    userAccessForm: FormGroup;

    constructor(private fb: FormBuilder) {
        this.userAccessForm = this.fb.group({
            employeeCode: [{ value: '', disabled: true }],
            firstName: [{ value: '', disabled: true }],
            lastName: [{ value: '', disabled: true }],
            email: [{ value: '', disabled: true }],
            phone: [{ value: '', disabled: true }],
            roleName: [{ value: '', disabled: true }],
            departmentName: [{ value: '', disabled: true }],
            designationName: [{ value: '', disabled: true }],
            password: ['', [Validators.required, Validators.minLength(6)]]
        });
    }

    ngOnChanges(changes: SimpleChanges): void {
        if (changes['employee'] && this.employee) {
            this.updateFormWithEmployeeData();
        }

        if (changes['registerUser'] && this.registerUser) {
            this.updateFormWithRegisterUserData();
        }
    }

    private updateFormWithEmployeeData(): void {
        if (this.employee) {
            this.userAccessForm.patchValue({
                employeeCode: this.employee.EmployeeCode || '',
                firstName: this.employee.FirstName || '',
                lastName: this.employee.LastName || '',
                email: this.employee.Email || '',
                phone: this.employee.Phone || '',
                roleName: this.getRoleName(this.employee.RoleId),
                departmentName: this.getDepartmentName(this.employee.DepartmentId),
                designationName: this.getDesignationName(this.employee.DesignationId),
                password: ''
            });
        }
    }

    private updateFormWithRegisterUserData(): void {
        if (this.registerUser) {
            this.userAccessForm.patchValue({
                password: this.registerUser.password || ''
            });
        }
    }

    private getRoleName(roleId: number | null | undefined): string {
        if (!roleId || !this.roles.length) return '';
        const role = this.roles.find(r => r.Id === roleId);
        return role ? role.Name : '';
    }

    private getDepartmentName(departmentId: number | null | undefined): string {
        if (!departmentId || !this.departments.length) return '';
        const department = this.departments.find(d => d.DepartmentId === departmentId);
        return department ? department.Name : '';
    }

    private getDesignationName(designationId: number | null | undefined): string {
        if (!designationId || !this.designations.length) return '';
        const designation = this.designations.find(d => d.DesignationId === designationId);
        return designation ? designation.Name : '';
    }

    hasError(controlName: string, errorName: string): boolean {
        const control = this.userAccessForm.get(controlName);
        return !!control && control.hasError(errorName) && control.touched;
    }

    prepareRegisterUser(): RegisterUser {
        const registerUser: RegisterUser = {
            ...(this.registerUser?.id && { id: this.registerUser.id }),
            employee_id: this.employee?.EmployeeId,
            first_name: this.employee?.FirstName ?? undefined,
            last_name: this.employee?.LastName ?? undefined,
            email: this.employee?.Email ?? undefined,
            phone: this.employee?.Phone ?? undefined,
            role_id: this.employee?.RoleId ?? undefined,
            department_id: this.employee?.DepartmentId ?? undefined,
            password: this.userAccessForm.get('password')?.value,
            is_active: true,
            ...(this.registerUser?.created_by && { created_by: this.registerUser.created_by })
        };

        Object.keys(registerUser).forEach(key => {
            if (registerUser[key as keyof RegisterUser] === undefined) {
                delete registerUser[key as keyof RegisterUser];
            }
        });

        return registerUser;
    }

    onSubmit(): void {
        if (this.userAccessForm.valid) {
            const registerUser = this.prepareRegisterUser();
            console.log('Prepared RegisterUser for API:', registerUser);
            this.saveUserAcess.emit(registerUser);
            this.onClose();
        } else {
            Object.keys(this.userAccessForm.controls).forEach(key => {
                const control = this.userAccessForm.get(key);
                control?.markAsTouched();
            });
        }
    }

    onClose(): void {
        this.close.emit();
        this.userAccessForm.reset();
    }
}