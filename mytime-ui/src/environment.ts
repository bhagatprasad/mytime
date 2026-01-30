export const environment = {
    production: false,
    baseUrl: 'https://mytime-docker.onrender.com/api/v1',
    UrlConstants: {
        // Authentication endpoints
        Authenticate: 'auth/AuthenticateUser',
        GenerateUserClaims: 'auth/GenarateUserClaims',
        ForgotPasswordAsync: 'auth/ForgotPasswordAsync',
        ResetPasswordAsync: 'auth/ResetPasswordAsync',
        ChangePasswordAsync: 'auth/ChangePasswordAsync',

        // User endpoints
        Users: {
            GetUsers: 'users/',
            GetUserById: 'users',
            RegisterUser: 'users/'
        },

        // Role endpoints
        Role: {
            GetRoleListAsync: 'roles/fetchAllRoles',
            GetRoleAsync: 'roles/fetchRole',
            InsertOrUpdateRoleAsync: 'roles/InsertOrUpdateRole',
            DeleteRoleAsync: 'roles/DeleteRole'
        },

        // Country endpoints
        Country: {
            GetCountry: 'countries/fetchCountry',
            GetAllCountries: 'countries/fetchAllCountries',
            GetActiveCountries: 'countries/fetchActiveCountries',
            GetCountries: 'countries/getCountries',
            CheckCountryExists: 'countries/checkCountryExists',
            GetCountryByCode: 'countries/getCountryByCode',
            InsertOrUpdateCountry: 'countries/InsertOrUpdateCountry',
            DeleteCountry: 'countries/DeleteCountry',
            CreateCountry: 'countries/create',
            UpdateCountry: 'countries/update',
            ToggleActiveStatus: 'countries/toggleActiveStatus',
            SearchCountries: 'countries/searchCountries',
            GetCountriesByIds: 'countries/getCountriesByIds'
        },

        // State endpoints
        State: {
            GetState: 'states/fetchState',
            GetAllStates: 'states/fetchAllStates',
            GetStates: 'states/getStates',
            InsertOrUpdateState: 'states/InsertOrUpdateState',
            DeleteState: 'states/DeleteState',
            CheckStateExists: 'states/checkStateExists',
            GetStatesByCountry: 'states/getStatesByCountry',
            GetStatesByCountryCode: 'states/getStatesByCountryCode',
            GetStateByCode: 'states/getStateByCode',
            ToggleActiveStatus: 'states/toggleActiveStatus',
            CreateState: 'states/create',
            UpdateState: 'states/update'
        },

        // City endpoints
        City: {
            GetCity: 'cities/fetchCity',
            GetCityWithRelations: 'cities/fetchCityWithRelations',
            GetAllCities: 'cities/fetchAllCities',
            GetActiveCities: 'cities/fetchActiveCities',
            GetCities: 'cities/getCities',
            InsertOrUpdateCity: 'cities/InsertOrUpdateCity',
            DeleteCity: 'cities/DeleteCity',
            CheckCityExists: 'cities/checkCityExists',
            GetCitiesByCountry: 'cities/getCitiesByCountry',
            GetCitiesByState: 'cities/getCitiesByState',
            GetCitiesByCountryAndState: 'cities/getCitiesByCountryAndState',
            GetCityByCode: 'cities/getCityByCode',
            ToggleActiveStatus: 'cities/toggleActiveStatus',
            CreateCity: 'cities/create',
            UpdateCity: 'cities/update',
            SearchCities: 'cities/searchCities'
        },

        // Department endpoints
        Department: {
            GetDepartment: 'departments/fetchDepartment',
            GetAllDepartments: 'departments/fetchAllDepartments',
            GetActiveDepartments: 'departments/fetchActiveDepartments',
            GetDepartments: 'departments/getDepartments',
            CheckDepartmentExists: 'departments/checkDepartmentExists',
            GetDepartmentByCode: 'departments/getDepartmentByCode',
            InsertOrUpdateDepartment: 'departments/InsertOrUpdateDepartment',
            DeleteDepartment: 'departments/DeleteDepartment',
            CreateDepartment: 'departments/create',
            UpdateDepartment: 'departments/update',
            ToggleActiveStatus: 'departments/toggleActiveStatus',
            SearchDepartments: 'departments/searchDepartments',
            GetDepartmentsByIds: 'departments/getDepartmentsByIds'
        },

        // Designation endpoints
        Designation: {
            GetDesignation: 'designations/fetchDesignation',
            GetAllDesignations: 'designations/fetchAllDesignations',
            GetActiveDesignations: 'designations/fetchActiveDesignations',
            GetDesignations: 'designations/getDesignations',
            CheckDesignationExists: 'designations/checkDesignationExists',
            GetDesignationByCode: 'designations/getDesignationByCode',
            InsertOrUpdateDesignation: 'designations/InsertOrUpdateDesignation',
            DeleteDesignation: 'designations/DeleteDesignation',
            CreateDesignation: 'designations/create',
            UpdateDesignation: 'designations/update',
            ToggleActiveStatus: 'designations/toggleActiveStatus',
            SearchDesignations: 'designations/searchDesignations',
            GetDesignationsByIds: 'designations/getDesignationsByIds'
        },

        // DocumentType endpoints
        DocumentType: {
            GetDocumentType: 'documenttypes/fetchDocumentType',
            GetAllDocumentTypes: 'documenttypes/fetchAllDocumentTypes',
            GetActiveDocumentTypes: 'documenttypes/fetchActiveDocumentTypes',
            GetDocumentTypes: 'documenttypes/getDocumentTypes',
            CheckDocumentTypeExists: 'documenttypes/checkDocumentTypeExists',
            InsertOrUpdateDocumentType: 'documenttypes/InsertOrUpdateDocumentType',
            DeleteDocumentType: 'documenttypes/DeleteDocumentType',
            CreateDocumentType: 'documenttypes/create',
            UpdateDocumentType: 'documenttypes/update',
            ToggleActiveStatus: 'documenttypes/toggleActiveStatus',
            SearchDocumentTypes: 'documenttypes/searchDocumentTypes',
            GetDocumentTypesByIds: 'documenttypes/getDocumentTypesByIds'
        },

        // HolidayCalendar endpoints
        HolidayCalendar: {
            GetHolidayCalendar: 'holiydacallender/fetchHolidayCalendar',
            GetAllHolidayCalendars: 'holiydacallender/fetchAllHolidayCalendars',
            GetActiveHolidayCalendars: 'holiydacallender/fetchActiveHolidayCalendars',
            GetHolidayCalendars: 'holiydacallender/getHolidayCalendars',
            CheckHolidayCalendarExists: 'holiydacallender/checkHolidayCalendarExists',
            GetHolidaysByYear: 'holiydacallender/getHolidaysByYear',
            GetHolidaysByDateRange: 'holiydacallender/getHolidaysByDateRange',
            GetHolidaysByMonth: 'holiydacallender/getHolidaysByMonth',
            GetUpcomingHolidays: 'holiydacallender/getUpcomingHolidays',
            IsHoliday: 'holiydacallender/isHoliday',
            InsertOrUpdateHolidayCalendar: 'holiydacallender/InsertOrUpdateHolidayCalendar',
            DeleteHolidayCalendar: 'holiydacallender/DeleteHolidayCalendar',
            CreateHolidayCalendar: 'holiydacallender/create',
            UpdateHolidayCalendar: 'holiydacallender/update',
            ToggleActiveStatus: 'holiydacallender/toggleActiveStatus',
            SearchHolidayCalendars: 'holiydacallender/searchHolidayCalendars',
            GetHolidayCalendarsByIds: 'holiydacallender/getHolidayCalendarsByIds'
        }
    }
};