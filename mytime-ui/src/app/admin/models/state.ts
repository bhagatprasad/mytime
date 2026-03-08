export interface State {
    StateId: number;
    CountryId: number;
    Name: string;
    Description: string;
    StateCode: string;
    CountryCode: string;
    IsActive?: boolean;
    CreatedBy?: number;
    CreatedOn?: Date;
    ModifiedBy?: number;
    ModifiedOn?: Date;
}