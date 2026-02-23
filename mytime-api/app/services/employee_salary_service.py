from sqlalchemy.orm import Session
from sqlalchemy import or_, asc, desc, func
from typing import Optional, List, Tuple, Dict, Any
from app.models.employee_salary import EmployeeSalary

class EmployeeSalaryService:
    """Service for EmployeeSalary operations - matching C# controller functionality"""
    
    @staticmethod
    def fetch_employee_salary(db: Session, employee_salary_id: int) -> Optional[EmployeeSalary]:
        """Get employee salary by ID - matches fetchEmployeeSalary in C#"""
        return db.query(EmployeeSalary).filter(EmployeeSalary.EmployeeSalaryId == employee_salary_id).first()
    
    @staticmethod
    def fetch_all_employee_salaries(db: Session) -> List[EmployeeSalary]:
        """Get all employee salaries - matches fetchAllEmployeeSalaries in C#"""
        return db.query(EmployeeSalary).all()
    
    @staticmethod
    def fetch_employee_salaries_by_employeeid(
        db: Session, employee_id: int
    ) -> List[EmployeeSalary]:
        """Get employee salaries by employee ID - matches getEmployeeSalariesByEmployeeId in C#"""
        return db.query(EmployeeSalary).filter(EmployeeSalary.EmployeeId == employee_id).all()