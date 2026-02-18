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
            GetStatesByCountry: 'states/getStatesByCountry/',
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
        },
        // Employee endpoints
        Employee: {
            // GET endpoints
            GetEmployee: 'employee/fetchEmployee',
            GetEmployeeByCode: 'employee/fetchEmployeeByCode',
            GetEmployeeByEmail: 'employee/fetchEmployeeByEmail',
            GetEmployeeByUserId: 'employee/fetchEmployeeByUserId',
            GetAllEmployees: 'employee/fetchAllEmployees',
            GetEmployees: 'employee/getEmployees',
            CheckEmployeeExists: 'employee/checkEmployeeExists',
            GetEmployeesByDepartment: 'employee/getEmployeesByDepartment',
            GetEmployeesByDesignation: 'employee/getEmployeesByDesignation',
            GetEmployeeStatistics: 'employee/employeeStatistics',
            GetActiveEmployees: 'employee/activeEmployees',
            ExportEmployees: 'employee/exportEmployees',

            // POST endpoints
            InsertOrUpdateEmployee: 'employee/InsertOrUpdateEmployee',
            SearchEmployees: 'employee/searchEmployees',
            CreateEmployee: 'employee/create',
            BulkUpdateDepartment: 'employee/bulkUpdateDepartment',

            // PUT endpoint
            UpdateEmployee: 'employee/update',

            // DELETE endpoints
            DeleteEmployee: 'employee/DeleteEmployee',
            SoftDeleteEmployee: 'employee/SoftDeleteEmployee',

            // PATCH endpoint
            UpdateActiveStatus: 'employee/updateActiveStatus'
        },

        // EmployeeAddress endpoints
        EmployeeAddress: {
            // GET endpoints
            GetEmployeeAddress: 'employeeaddress/fetchEmployeeAddress',
            GetAddressesByEmployee: 'employeeaddress/fetchAddressesByEmployee',
            GetActiveAddressesByEmployee: 'employeeaddress/fetchActiveAddressesByEmployee',
            GetAllEmployeeAddresses: 'employeeaddress/fetchAllEmployeeAddresses',
            GetEmployeeAddresses: 'employeeaddress/getEmployeeAddresses',
            CheckEmployeeAddressExists: 'employeeaddress/checkEmployeeAddressExists',
            GetPrimaryAddress: 'employeeaddress/getPrimaryAddress',

            // POST endpoints
            InsertOrUpdateEmployeeAddress: 'employeeaddress/InsertOrUpdateEmployeeAddress',
            CreateBulkAddresses: 'employeeaddress/createBulkAddresses',
            CreateEmployeeAddress: 'employeeaddress/create',
            SearchEmployeeAddresses: 'employeeaddress/searchEmployeeAddresses',

            // PUT endpoint
            UpdateEmployeeAddress: 'employeeaddress/update',

            // DELETE endpoint
            DeleteEmployeeAddress: 'employeeaddress/DeleteEmployeeAddress',

            // PATCH endpoints
            SoftDeleteEmployeeAddress: 'employeeaddress/SoftDeleteEmployeeAddress',
            SetPrimaryAddress: 'employeeaddress/setPrimaryAddress'
        },

        // EmployeeEducation endpoints
        EmployeeEducation: {
            // GET endpoints
            GetEmployeeEducation: 'employeeeducation/fetchEmployeeEducation',
            GetEducationsByEmployee: 'employeeeducation/fetchEducationsByEmployee',
            GetActiveEducationsByEmployee: 'employeeeducation/fetchActiveEducationsByEmployee',
            GetHighestEducationByEmployee: 'employeeeducation/fetchHighestEducationByEmployee',
            GetAllEmployeeEducations: 'employeeeducation/fetchAllEmployeeEducations',
            GetEmployeeEducations: 'employeeeducation/getEmployeeEducations',
            CheckEmployeeEducationExists: 'employeeeducation/checkEmployeeEducationExists',
            GetEmployeeEducationSummary: 'employeeeducation/getEmployeeEducationSummary',
            GetEducationStatistics: 'employeeeducation/educationStatistics',
            SearchByDegree: 'employeeeducation/searchByDegree',
            SearchByInstitution: 'employeeeducation/searchByInstitution',

            // POST endpoints
            InsertOrUpdateEmployeeEducation: 'employeeeducation/InsertOrUpdateEmployeeEducation',
            CreateBulkEducations: 'employeeeducation/createBulkEducations',
            CreateEmployeeEducation: 'employeeeducation/create',
            SearchEmployeeEducations: 'employeeeducation/searchEmployeeEducations',

            // PUT endpoint
            UpdateEmployeeEducation: 'employeeeducation/update',

            // DELETE endpoint
            DeleteEmployeeEducation: 'employeeeducation/DeleteEmployeeEducation',

            // PATCH endpoint
            SoftDeleteEmployeeEducation: 'employeeeducation/SoftDeleteEmployeeEducation'
        },

        // EmployeeEmployment endpoints
        EmployeeEmployment: {
            // GET endpoints
            GetEmployeeEmployment: 'employeeemployment/fetchEmployeeEmployment',
            GetEmploymentsByEmployee: 'employeeemployment/fetchEmploymentsByEmployee',
            GetActiveEmploymentsByEmployee: 'employeeemployment/fetchActiveEmploymentsByEmployee',
            GetLatestEmploymentByEmployee: 'employeeemployment/fetchLatestEmploymentByEmployee',
            GetAllEmployeeEmployments: 'employeeemployment/fetchAllEmployeeEmployments',
            GetEmployeeEmployments: 'employeeemployment/getEmployeeEmployments',
            CheckEmployeeEmploymentExists: 'employeeemployment/checkEmployeeEmploymentExists',
            GetEmployeeEmploymentSummary: 'employeeemployment/getEmployeeEmploymentSummary',
            GetEmploymentStatistics: 'employeeemployment/employmentStatistics',
            SearchByCompany: 'employeeemployment/searchByCompany',
            SearchByDesignation: 'employeeemployment/searchByDesignation',
            GetEmployeesByPreviousCompany: 'employeeemployment/employeesByPreviousCompany',
            CalculateTotalExperience: 'employeeemployment/calculateTotalExperience',

            // POST endpoints
            InsertOrUpdateEmployeeEmployment: 'employeeemployment/InsertOrUpdateEmployeeEmployment',
            CreateBulkEmployments: 'employeeemployment/createBulkEmployments',
            CreateEmployeeEmployment: 'employeeemployment/create',
            SearchEmployeeEmployments: 'employeeemployment/searchEmployeeEmployments',

            // PUT endpoint
            UpdateEmployeeEmployment: 'employeeemployment/update',

            // DELETE endpoint
            DeleteEmployeeEmployment: 'employeeemployment/DeleteEmployeeEmployment',

            // PATCH endpoint
            SoftDeleteEmployeeEmployment: 'employeeemployment/SoftDeleteEmployeeEmployment'
        },

        EmployeeEmergencyContact: {
            GetEmployeeEmergencyContact: 'employeeemergencycontact/fetchEmployeeEmergencyContact',
            GetContactsByEmployee: 'employeeemergencycontact/fetchContactsByEmployee',
            GetActiveContactsByEmployee: 'employeeemergencycontact/fetchActiveContactsByEmployee',
            GetPrimaryEmergencyContact: 'employeeemergencycontact/fetchPrimaryEmergencyContact',
            GetAllEmployeeEmergencyContacts: 'employeeemergencycontact/fetchAllEmployeeEmergencyContacts',
            GetEmployeeEmergencyContacts: 'employeeemergencycontact/getEmployeeEmergencyContacts',
            CheckEmployeeEmergencyContactExists: 'employeeemergencycontact/checkEmployeeEmergencyContactExists',
            GetEmployeeEmergencyContactsSummary: 'employeeemergencycontact/getEmployeeEmergencyContactsSummary',
            GetEmergencyContactStatistics: 'employeeemergencycontact/emergencyContactStatistics',
            SearchByRelation: 'employeeemergencycontact/searchByRelation',
            GetEmployeesWithoutEmergencyContacts: 'employeeemergencycontact/employeesWithoutEmergencyContacts',
            InsertOrUpdateEmployeeEmergencyContact: 'employeeemergencycontact/InsertOrUpdateEmployeeEmergencyContact',
            CreateBulkEmergencyContacts: 'employeeemergencycontact/createBulkEmergencyContacts',
            CreateEmployeeEmergencyContact: 'employeeemergencycontact/create',
            SearchEmployeeEmergencyContacts: 'employeeemergencycontact/searchEmployeeEmergencyContacts',
            UpdateEmployeeEmergencyContact: 'employeeemergencycontact/update',
            DeleteEmployeeEmergencyContact: 'employeeemergencycontact/DeleteEmployeeEmergencyContact',
            SoftDeleteEmployeeEmergencyContact: 'employeeemergencycontact/SoftDeleteEmployeeEmergencyContact',
            SetAsPrimaryContact: 'employeeemergencycontact/setAsPrimaryContact'
        },

        EmployeeSalaryStructure: {
            GetEmployeeSalaryStructure: 'employeesalarystructure/fetchEmployeeSalaryStructure',
            GetSalaryStructureByEmployee: 'employeesalarystructure/fetchSalaryStructureByEmployee',
            GetAllSalaryStructuresByEmployee: 'employeesalarystructure/fetchAllSalaryStructuresByEmployee',
            GetActiveSalaryStructures: 'employeesalarystructure/fetchActiveSalaryStructures',
            GetAllEmployeeSalaryStructures: 'employeesalarystructure/fetchAllEmployeeSalaryStructures',
            GetEmployeeSalaryStructures: 'employeesalarystructure/getEmployeeSalaryStructures',
            CheckEmployeeSalaryStructureExists: 'employeesalarystructure/checkEmployeeSalaryStructureExists',
            GetSalaryBreakdown: 'employeesalarystructure/getSalaryBreakdown',
            GetSalaryStatistics: 'employeesalarystructure/salaryStatistics',
            GetSalaryComparisonReport: 'employeesalarystructure/salaryComparisonReport',
            GetEmployeesWithoutSalaryStructure: 'employeesalarystructure/employeesWithoutSalaryStructure',
            CalculateNetSalary: 'employeesalarystructure/calculateNetSalary',
            GetPayrollSummary: 'employeesalarystructure/payrollSummary',
            InsertOrUpdateEmployeeSalaryStructure: 'employeesalarystructure/InsertOrUpdateEmployeeSalaryStructure',
            CreateEmployeeSalaryStructure: 'employeesalarystructure/create',
            SearchEmployeeSalaryStructures: 'employeesalarystructure/searchEmployeeSalaryStructures',
            UpdateEmployeeSalaryStructure: 'employeesalarystructure/update',
            DeleteEmployeeSalaryStructure: 'employeesalarystructure/DeleteEmployeeSalaryStructure',
            SoftDeleteEmployeeSalaryStructure: 'employeesalarystructure/SoftDeleteEmployeeSalaryStructure'
        },
        Backblaze: {
            endpoint: 's3.us-east-005.backblazeb2.com',
            keyId: '332633bece97',
            applicationKey: '00537f0af2eea022537d2605ef4ed7557424c2b859',
            bucketId: '9393a26623636bce9cce0917',
            bucketName: 'mytime'
        },
        EmployeeDocuments: {
            GetEmployeeDocuments: 'employeedocuments/fetchEmployeeDocuments',
            GetEmployeeDocument: 'employeedocuments/fetchEmployeeDocument',
            GetDocumentsByEmployee: 'employeedocuments/fetchDocumentsByEmployee',
            InsertOrUpdateEmployeeDocument: 'employeedocuments/InsertOrUpdateEmployeeDocument',
            DeleteEmployeeDocument: 'employeedocuments/DeleteEmployeeDocument'
        }

    }
};