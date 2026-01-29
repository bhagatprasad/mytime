import { ApplicationUser } from "./application-user";

interface UserContext {
  isAuthenticated: boolean | null;
  user: ApplicationUser | null;
  isAdmin: boolean;
  isAdministrator: boolean;
  isRegularAdmin: boolean;
  userRoleName: string;
}
