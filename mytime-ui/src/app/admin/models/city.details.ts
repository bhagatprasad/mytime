import { City } from "./city";

export interface CityDetails extends City {
    CountryName: string;
    StateName: string;
}