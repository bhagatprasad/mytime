export interface User {
    Id: number;
    EmployeeId?: number;
    FirstName?: string;
    LastName?: string;
    Email?: string;
    Phone?: string;
    DepartmentId?: number;
    RoleId?: number;
    PasswordHash?: string;
    PasswordSalt?: string;
    PasswordlastChangedOn?: Date;
    PasswordLastChangedBY?: number;
    UserWorngPasswordCount?: number;
    UserLastWrongPasswordOn?: Date;
    IsBlocked: boolean;
    IsActive: boolean;
    CreatedBy?: number;
    CreatedOn?: Date;
    ModifiedBy?: number;
    ModifiedOn?: Date;
}