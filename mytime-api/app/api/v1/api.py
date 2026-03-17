# app/api/v1/api.py - Ensure this has authorization
from fastapi import APIRouter, Depends

print("=" * 50)
print("DEBUG: Loading api.py with authorization")
print("=" * 50)

# Try to import get_current_user
try:
    from app.core.dependencies import get_current_user
    HAS_AUTH = True
    print("✅ get_current_user imported successfully")
except ImportError as e:
    HAS_AUTH = False
    print(f"⚠️  get_current_user import failed: {e}")
    
    # Create a dummy dependency for development
    async def get_current_user():
        return {"username": "test", "roles": ["admin"]}

# Import routers
try:
    from app.api.v1.routers import leave_routes,taskitem
     # Authentication & User Management
    from app.api.v1.routers import auth, user, roles
    
    # AI & ML Features
    from app.api.v1.routers import llm, vision, audio, embeddings
    
    # External Services
    from app.api.v1.routers import rss, backblaze_upload
    
    # Master Data - Location
    from app.api.v1.routers import country, state, city
    
    # Master Data - Employee Related
    from app.api.v1.routers import designation, department, document_type, holiday_calendar
    
    # Employee Management
    from app.api.v1.routers import employee
    from app.api.v1.routers import employee_address, employee_education
    from app.api.v1.routers import employee_emergency_contact, employee_employment
    from app.api.v1.routers import employee_salary_structure, employee_document
    from app.api.v1.routers import employee_salary, monthly_salary
    
    # Project Management
    from app.api.v1.routers import project, taskcode,user_profile_image, leavetype
    print("✅ All routers imported")
except ImportError as e:
    print(f"❌ Router import error: {e}")
    # Create dummy routers for development
    from fastapi import APIRouter
    
    class DummyRouter:
        def __init__(self):
            self.router = APIRouter()
    
    auth = DummyRouter()
    user = DummyRouter()
    roles = DummyRouter()
    llm = DummyRouter()
    vision = DummyRouter()
    audio = DummyRouter()
    embeddings = DummyRouter()
    rss = DummyRouter()
    country = DummyRouter()
    state = DummyRouter()
    city = DummyRouter()
    department = DummyRouter()
    designation = DummyRouter()
    document_type = DummyRouter()
    holiday_calendar = DummyRouter()
    employee = DummyRouter()
    employee_address = DummyRouter()
    employee_education = DummyRouter()
    employee_employment = DummyRouter()
    employee_emergency_contact = DummyRouter()
    employee_salary_structure = DummyRouter()
    employee_document = DummyRouter()
    backblaze_upload = DummyRouter()
    employee_salary = DummyRouter()
    monthly_salary = DummyRouter()
    project = DummyRouter()
    taskitem = DummyRouter()
    taskcode =DummyRouter()
    user_profile_image = DummyRouter()
    leave_routes=DummyRouter()
    leavetype=DummyRouter()
# Create main router
api_router = APIRouter()

# Public routes - authentication should be public
api_router.include_router(auth.router, tags=["authentication"])

# Protected routes
if HAS_AUTH:
    from fastapi import APIRouter
    
    # Create protected routers with dependencies
    users_protected = APIRouter(dependencies=[Depends(get_current_user)])
    users_protected.include_router(user.router)
    
    roles_protected = APIRouter(dependencies=[Depends(get_current_user)])
    roles_protected.include_router(roles.router)
    
    countries_protected = APIRouter(dependencies=[Depends(get_current_user)])
    countries_protected.include_router(country.router)

    states_protected = APIRouter(dependencies=[Depends(get_current_user)])
    states_protected.include_router(state.router)

    cities_protected = APIRouter(dependencies=[Depends(get_current_user)])
    cities_protected.include_router(city.router)

    department_protected = APIRouter(dependencies=[Depends(get_current_user)])
    department_protected.include_router(department.router)

    designation_protected = APIRouter(dependencies=[Depends(get_current_user)])
    designation_protected.include_router(designation.router)

    documenttype_protected = APIRouter(dependencies=[Depends(get_current_user)])
    documenttype_protected.include_router(document_type.router)

    holiydacallender_protected = APIRouter(dependencies=[Depends(get_current_user)])
    holiydacallender_protected.include_router(holiday_calendar.router)
    

    employee_protected = APIRouter(dependencies=[Depends(get_current_user)])
    employee_protected.include_router(employee.router)


    employee_address_protected = APIRouter(dependencies=[Depends(get_current_user)])
    employee_address_protected.include_router(employee_address.router)


    employee_education_protected = APIRouter(dependencies=[Depends(get_current_user)])
    employee_education_protected.include_router(employee_education.router)


    employee_employment_protected = APIRouter(dependencies=[Depends(get_current_user)])
    employee_employment_protected.include_router(employee_employment.router)


    employee_emergency_contact_protected = APIRouter(dependencies=[Depends(get_current_user)])
    employee_emergency_contact_protected.include_router(employee_emergency_contact.router)


    employee_salary_structure_protected = APIRouter(dependencies=[Depends(get_current_user)])
    employee_salary_structure_protected.include_router(employee_salary_structure.router)

    employee_documents_protected = APIRouter(dependencies=[Depends(get_current_user)])
    employee_documents_protected.include_router(employee_document.router)

    backblaze_upload_protected = APIRouter(dependencies=[Depends(get_current_user)])
    backblaze_upload_protected.include_router(backblaze_upload.router)


    employee_salary_protected = APIRouter(dependencies=[Depends(get_current_user)])
    employee_salary_protected.include_router(employee_salary.router)
            
    monthly_salary_protected = APIRouter(dependencies=[Depends(get_current_user)])
    monthly_salary_protected.include_router(monthly_salary.router)

    project_protected = APIRouter(dependencies=[Depends(get_current_user)])
    project_protected.include_router(project.router)

    taskcode_protected = APIRouter(dependencies=[Depends(get_current_user)])
    taskcode_protected.include_router(taskcode.router)

    user_profile_image_protected = APIRouter(dependencies=[Depends(get_current_user)])
    user_profile_image_protected.include_router(user_profile_image.router)

    task_item_protected = APIRouter(dependencies=[Depends(get_current_user)])
    task_item_protected.include_router(taskitem.router)

    leave_routes_protected = APIRouter(dependencies=[Depends(get_current_user)])
    leave_routes_protected.include_router(leave_routes.router)


    leavetype_protected = APIRouter(dependencies=[Depends(get_current_user)])
    leavetype_protected.include_router(leavetype.router)
            
    # Include protected routes
    api_router.include_router(users_protected, prefix="/users", tags=["users"])
    api_router.include_router(roles_protected, prefix="/roles", tags=["roles"])
    api_router.include_router(countries_protected, prefix="/countries", tags=["countries"])
    api_router.include_router(states_protected, prefix="/states", tags=["states"])
    api_router.include_router(cities_protected, prefix="/cities", tags=["cities"])
    api_router.include_router(department_protected, prefix="/departments", tags=["departments"])
    api_router.include_router(designation_protected, prefix="/designations", tags=["designations"])
    api_router.include_router(documenttype_protected, prefix="/documenttypes", tags=["documenttypes"])
    api_router.include_router(holiydacallender_protected, prefix="/holiydacallender", tags=["holiydacallender"])
    api_router.include_router(employee_protected, prefix="/employee", tags=["employee"])
    api_router.include_router(employee_address_protected, prefix="/employeeaddress", tags=["employeeaddress"])
    api_router.include_router(employee_education_protected, prefix="/employeeeducation", tags=["employeeeducation"])
    api_router.include_router(employee_employment_protected, prefix="/employeeemployment", tags=["employeeemployment"])
    api_router.include_router(employee_emergency_contact_protected, prefix="/employeeemergencycontact", tags=["employeeemergencycontact"])
    api_router.include_router(employee_salary_structure_protected, prefix="/employeesalarystructure", tags=["employeesalarystructure"])
    api_router.include_router(employee_documents_protected, prefix="/employeedocuments", tags=["employeedocuments"])
    api_router.include_router(backblaze_upload_protected, prefix="/backblaze", tags=["backblaze"])
    api_router.include_router(monthly_salary_protected, prefix="/monthlysalary", tags=["monthlysalary"])
    api_router.include_router(employee_salary_protected, prefix="/employeesalary", tags=["employeesalary"])
    api_router.include_router(project_protected, prefix="/project", tags=["project"])
    api_router.include_router(taskcode_protected, prefix="/taskcode", tags=["taskcode"])
    api_router.include_router(user_profile_image_protected, prefix="/userprofileimage", tags=["userprofileimage"])
    api_router.include_router(task_item_protected, prefix="/itemitem", tags=["taskitem"])
    api_router.include_router(leave_routes_protected, prefix="/leaves", tags=["Leaves"])
    api_router.include_router(leavetype_protected, prefix="/leavetype", tags=["leavetype"])
else:
    # Development mode - include without auth
    api_router.include_router(user.router, prefix="/users", tags=["users"])
    api_router.include_router(roles.router, prefix="/roles", tags=["roles"])
    api_router.include_router(country.router, prefix="/countries", tags=["countries"])
    api_router.include_router(state.router, prefix="/states", tags=["states"])
    api_router.include_router(city.router, prefix="/cities", tags=["cities"])
    api_router.include_router(department.router, prefix="/departments", tags=["departments"])
    api_router.include_router(designation.router, prefix="/designations", tags=["designations"])
    api_router.include_router(document_type.router, prefix="/documenttypes", tags=["documenttypes"])
    api_router.include_router(holiday_calendar.router, prefix="/holiydacallender", tags=["holiydacallender"])
    api_router.include_router(employee.router, prefix="/employee", tags=["employee"])
    api_router.include_router(employee_address.router, prefix="/employeeaddress", tags=["employeeaddress"])
    api_router.include_router(employee_education.router, prefix="/employeeeducation", tags=["employeeeducation"])
    api_router.include_router(employee_employment.router, prefix="/employeeemployment", tags=["employeeemployment"])
    api_router.include_router(employee_emergency_contact.router, prefix="/employeeemergencycontact", tags=["employeeemergencycontact"])
    api_router.include_router(employee_salary_structure.router, prefix="/employeesalarystructure", tags=["employeesalarystructure"])
    api_router.include_router(employee_document.router, prefix="/employeedocuments", tags=["employeedocuments"])
    api_router.include_router(backblaze_upload.router, prefix="/backblaze", tags=["backblaze"])
    api_router.include_router(employee_salary.router, prefix="/employeesalary", tags=["employeesalary"])
    api_router.include_router(monthly_salary.router, prefix="/monthlysalary", tags=["monthlysalary"])
    api_router.include_router(project.router, prefix="/project", tags=["project"])
    api_router.include_router(taskcode.router, prefix="/taskcode", tags=["taskcode"])
    api_router.include_router(user_profile_image.router, prefix="/userprofileimage", tags=["userprofileimage"])
    api_router.include_router(taskitem.router, prefix="/taskitem", tags=["taskitem"])
    api_router.include_router(leave_routes.router, prefix="/leaves", tags=["leaves"])
    api_router.include_router(leavetype.router, prefix="/leavetype", tags=["leavetype"])

# AI routes - decide if these should be public or protected
# For now, making them public for development
api_router.include_router(llm.router, prefix="/llm", tags=["llm"])
api_router.include_router(vision.router, prefix="/vision", tags=["vision"])
api_router.include_router(audio.router, prefix="/audio", tags=["audio"])
api_router.include_router(embeddings.router, prefix="/embeddings", tags=["embeddings"])
api_router.include_router(rss.router, prefix="/rss", tags=["rss"])

# Test endpoints
@api_router.get("/test", tags=["test"])
async def api_test():
    return {"message": "API test", "status": "working"}

@api_router.get("/protected-test", tags=["test"])
async def protected_test(current_user = Depends(get_current_user) if HAS_AUTH else None):
    return {
        "message": "Protected endpoint",
        "user": current_user if current_user else "No auth",
        "protected": HAS_AUTH
    }

print(f"✅ API routes loaded at /api/v1")
print(f"✅ Auth enabled: {HAS_AUTH}")