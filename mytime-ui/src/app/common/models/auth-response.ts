export interface AuthResponse
{
    jwtToken: string;
    validUser:boolean;
    validPassword:boolean;
    isActive:boolean;
    statusCode:number;
    statusMessage:string;
}