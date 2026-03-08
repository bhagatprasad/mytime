export interface EmployeeAddress {
  EmployeeAddressId: number;
  EmployeeId?: number | null;
  HNo?: string | null;
  AddressLineOne?: string | null;
  AddressLineTwo?: string | null;
  Landmark?: string | null;
  CityId?: number | null;
  StateId?: number | null;
  CountryId?: number | null;
  Zipcode?: string | null;
  CreatedOn?: string | null;
  CreatedBy?: number | null;
  ModifiedOn?: string | null;
  ModifiedBy?: number | null;
  IsActive?: boolean | null;
}
