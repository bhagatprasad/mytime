export interface AuthResponse {
  jwt_token: string;
  valid_user: boolean;
  valid_password: boolean;
  is_active: boolean;
  status_code: string;
  status_message: string;
}