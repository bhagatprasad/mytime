import { User } from "./user";

export interface UserDeetails extends User {
    DepartmentName?: string;
    RoleName?: string;
}