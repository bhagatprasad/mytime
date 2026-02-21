export interface RegisterUser {
    id?: number;
    password?: string;
    employee_id?: number;
    first_name?: string;
    last_name?: string;
    role_id?: number;
    department_id?: number;
    email?: string;
    phone?: string;
    is_active?: boolean;
    created_by?: number;
}