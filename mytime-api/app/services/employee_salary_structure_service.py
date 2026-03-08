from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, asc, desc, func, case, and_
from typing import Optional, List, Tuple, Dict, Any
from datetime import datetime
from decimal import Decimal

from app.models.employee_salary_structure import EmployeeSalaryStructure
from app.models.employee import Employee
from app.schemas.employee_salary_structure_schemas import (
    EmployeeSalaryStructureCreate, 
    EmployeeSalaryStructureUpdate
)

class EmployeeSalaryStructureService:
    """Service for EmployeeSalaryStructure operations"""
    
    @staticmethod
    def fetch_employee_salary_structure(
        db: Session, 
        employee_salary_structure_id: int
    ) -> Optional[EmployeeSalaryStructure]:
        """Get employee salary structure by ID"""
        return db.query(EmployeeSalaryStructure).filter(
            EmployeeSalaryStructure.EmployeeSalaryStructureId == employee_salary_structure_id
        ).first()
    
    @staticmethod
    def fetch_salary_structure_by_employee(
        db: Session, 
        employee_id: int
    ) -> Optional[EmployeeSalaryStructure]:
        """Get salary structure for a specific employee"""
        return db.query(EmployeeSalaryStructure).filter(
            EmployeeSalaryStructure.EmployeeId == employee_id,
            EmployeeSalaryStructure.IsActive == True
        ).first()
    
    @staticmethod
    def fetch_all_salary_structures_by_employee(
        db: Session, 
        employee_id: int
    ) -> List[EmployeeSalaryStructure]:
        """Get all salary structures for a specific employee"""
        return db.query(EmployeeSalaryStructure).filter(
            EmployeeSalaryStructure.EmployeeId == employee_id
        ).order_by(
            desc(EmployeeSalaryStructure.CreatedOn)
        ).all()
    
    @staticmethod
    def fetch_active_salary_structures(db: Session) -> List[EmployeeSalaryStructure]:
        """Get all active salary structures"""
        return db.query(EmployeeSalaryStructure).filter(
            EmployeeSalaryStructure.IsActive == True
        ).all()
    
    @staticmethod
    def fetch_all_employee_salary_structures(db: Session) -> List[EmployeeSalaryStructure]:
        """Get all employee salary structures"""
        return db.query(EmployeeSalaryStructure).all()
    
    @staticmethod
    def get_employee_salary_structures_with_pagination(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        employee_id: Optional[int] = None,
        department_id: Optional[int] = None,
        designation_id: Optional[int] = None,
        min_basic: Optional[Decimal] = None,
        max_basic: Optional[Decimal] = None,
        is_active: Optional[bool] = None,
        has_pan: Optional[bool] = None,
        has_bank_account: Optional[bool] = None,
        sort_by: str = "EmployeeSalaryStructureId",
        sort_order: str = "desc"
    ) -> Tuple[List[EmployeeSalaryStructure], int]:
        """Get paginated employee salary structures with filtering and sorting"""
        query = db.query(EmployeeSalaryStructure)
        
        # Join with Employee table for department/designation filters
        if department_id or designation_id:
            query = query.join(Employee, EmployeeSalaryStructure.EmployeeId == Employee.EmployeeId)
        
        # Apply search filter
        if search:
            search_term = f"%{search}%"
            # Search in related employee fields
            query = query.filter(
                or_(
                    func.coalesce(EmployeeSalaryStructure.PAN, '').ilike(search_term),
                    func.coalesce(EmployeeSalaryStructure.BankAccount, '').ilike(search_term),
                    func.coalesce(EmployeeSalaryStructure.BankName, '').ilike(search_term),
                    func.coalesce(EmployeeSalaryStructure.UAN, '').ilike(search_term),
                    func.coalesce(EmployeeSalaryStructure.PFNO, '').ilike(search_term)
                )
            )
        
        # Apply employee filter
        if employee_id:
            query = query.filter(EmployeeSalaryStructure.EmployeeId == employee_id)
        
        # Apply department filter
        if department_id:
            query = query.filter(Employee.DepartmentId == department_id)
        
        # Apply designation filter
        if designation_id:
            query = query.filter(Employee.DesignationId == designation_id)
        
        # Apply basic salary filters
        if min_basic:
            query = query.filter(EmployeeSalaryStructure.BASIC >= min_basic)
        if max_basic:
            query = query.filter(EmployeeSalaryStructure.BASIC <= max_basic)
        
        # Apply active filter
        if is_active is not None:
            query = query.filter(EmployeeSalaryStructure.IsActive == is_active)
        
        # Apply PAN filter
        if has_pan is not None:
            if has_pan:
                query = query.filter(EmployeeSalaryStructure.PAN.isnot(None))
            else:
                query = query.filter(EmployeeSalaryStructure.PAN.is_(None))
        
        # Apply bank account filter
        if has_bank_account is not None:
            if has_bank_account:
                query = query.filter(EmployeeSalaryStructure.BankAccount.isnot(None))
            else:
                query = query.filter(EmployeeSalaryStructure.BankAccount.is_(None))
        
        # Get total count
        total = query.count()
        
        # Apply sorting
        sort_column = getattr(EmployeeSalaryStructure, sort_by, EmployeeSalaryStructure.EmployeeSalaryStructureId)
        if sort_order.lower() == "asc":
            query = query.order_by(asc(sort_column))
        else:
            query = query.order_by(desc(sort_column))
        
        # Apply pagination
        items = query.offset(skip).limit(limit).all()
        
        return items, total
    
    @staticmethod
    def calculate_salary_totals(salary_structure: EmployeeSalaryStructure) -> Dict[str, Decimal]:
        """Calculate salary totals for a salary structure"""
        # Calculate gross earnings
        gross_earnings = sum([
            salary_structure.BASIC or 0,
            salary_structure.HRA or 0,
            salary_structure.CONVEYANCE or 0,
            salary_structure.MEDICALALLOWANCE or 0,
            salary_structure.SPECIALALLOWANCE or 0,
            salary_structure.SPECIALBONUS or 0,
            salary_structure.STATUTORYBONUS or 0,
            salary_structure.OTHERS or 0
        ])
        
        # Calculate gross deductions
        gross_deductions = sum([
            salary_structure.PF or 0,
            salary_structure.ESIC or 0,
            salary_structure.PROFESSIONALTAX or 0,
            salary_structure.GroupHealthInsurance or 0
        ])
        
        # Calculate net take-home
        net_takehome = gross_earnings - gross_deductions
        
        return {
            "GROSSEARNINGS": Decimal(str(gross_earnings)),
            "GROSSDEDUCTIONS": Decimal(str(gross_deductions)),
            "NETTAKEHOME": Decimal(str(net_takehome))
        }
    
    @staticmethod
    def insert_or_update_employee_salary_structure(db: Session, salary_data: dict) -> Dict[str, Any]:
        """Insert or update employee salary structure"""
        employee_salary_structure_id = salary_data.get('EmployeeSalaryStructureId')
        
        if employee_salary_structure_id:
            # Update existing salary structure
            db_salary = db.query(EmployeeSalaryStructure).filter(
                EmployeeSalaryStructure.EmployeeSalaryStructureId == employee_salary_structure_id
            ).first()
            
            if not db_salary:
                return {"success": False, "message": "Employee salary structure not found", "salary": None}
            
            # Update only non-null values
            for key, value in salary_data.items():
                if key != 'EmployeeSalaryStructureId' and value is not None:
                    setattr(db_salary, key, value)
            
            # Set ModifiedOn timestamp
            db_salary.ModifiedOn = datetime.utcnow()
            
            # Calculate totals
            totals = EmployeeSalaryStructureService.calculate_salary_totals(db_salary)
            db_salary.GROSSEARNINGS = totals["GROSSEARNINGS"]
            db_salary.GROSSDEDUCTIONS = totals["GROSSDEDUCTIONS"]
            
            db.commit()
            db.refresh(db_salary)
            return {
                "success": True, 
                "message": "Employee salary structure updated successfully",
                "salary": db_salary,
                "net_takehome": totals["NETTAKEHOME"]
            }
        else:
            # Create new salary structure
            # Remove EmployeeSalaryStructureId if present in create mode
            salary_data.pop('EmployeeSalaryStructureId', None)
            
            # Set CreatedOn timestamp if not provided
            if 'CreatedOn' not in salary_data:
                salary_data['CreatedOn'] = datetime.utcnow()
            
            # Calculate totals before creating
            temp_salary = EmployeeSalaryStructure(**salary_data)
            totals = EmployeeSalaryStructureService.calculate_salary_totals(temp_salary)
            salary_data['GROSSEARNINGS'] = totals["GROSSEARNINGS"]
            salary_data['GROSSDEDUCTIONS'] = totals["GROSSDEDUCTIONS"]
            
            db_salary = EmployeeSalaryStructure(**salary_data)
            db.add(db_salary)
            db.commit()
            db.refresh(db_salary)
            return {
                "success": True, 
                "message": "Employee salary structure created successfully",
                "salary": db_salary,
                "net_takehome": totals["NETTAKEHOME"]
            }
    
    @staticmethod
    def delete_employee_salary_structure(db: Session, employee_salary_structure_id: int) -> Dict[str, Any]:
        """Delete employee salary structure"""
        db_salary = db.query(EmployeeSalaryStructure).filter(
            EmployeeSalaryStructure.EmployeeSalaryStructureId == employee_salary_structure_id
        ).first()
        
        if not db_salary:
            return {"success": False, "message": "Employee salary structure not found"}
        
        db.delete(db_salary)
        db.commit()
        return {"success": True, "message": "Employee salary structure deleted successfully"}
    
    @staticmethod
    def soft_delete_employee_salary_structure(
        db: Session, 
        employee_salary_structure_id: int, 
        modified_by: int
    ) -> Dict[str, Any]:
        """Soft delete employee salary structure (set IsActive = False)"""
        db_salary = db.query(EmployeeSalaryStructure).filter(
            EmployeeSalaryStructure.EmployeeSalaryStructureId == employee_salary_structure_id
        ).first()
        
        if not db_salary:
            return {"success": False, "message": "Employee salary structure not found"}
        
        db_salary.IsActive = False
        db_salary.ModifiedBy = modified_by
        db_salary.ModifiedOn = datetime.utcnow()
        
        db.commit()
        db.refresh(db_salary)
        return {
            "success": True, 
            "message": "Employee salary structure deactivated successfully",
            "salary": db_salary
        }
    
    @staticmethod
    def create_employee_salary_structure(
        db: Session, 
        salary: EmployeeSalaryStructureCreate
    ) -> EmployeeSalaryStructure:
        """Create new employee salary structure using Pydantic schema"""
        salary_data = salary.model_dump(exclude_none=True)
        
        # Set CreatedOn timestamp if not provided
        if 'CreatedOn' not in salary_data:
            salary_data['CreatedOn'] = datetime.utcnow()
        
        # Calculate totals
        temp_salary = EmployeeSalaryStructure(**salary_data)
        totals = EmployeeSalaryStructureService.calculate_salary_totals(temp_salary)
        salary_data['GROSSEARNINGS'] = totals["GROSSEARNINGS"]
        salary_data['GROSSDEDUCTIONS'] = totals["GROSSDEDUCTIONS"]
        
        db_salary = EmployeeSalaryStructure(**salary_data)
        db.add(db_salary)
        db.commit()
        db.refresh(db_salary)
        return db_salary
    
    @staticmethod
    def update_employee_salary_structure(
        db: Session, 
        employee_salary_structure_id: int, 
        salary: EmployeeSalaryStructureUpdate
    ) -> Optional[EmployeeSalaryStructure]:
        """Update existing employee salary structure using Pydantic schema"""
        db_salary = db.query(EmployeeSalaryStructure).filter(
            EmployeeSalaryStructure.EmployeeSalaryStructureId == employee_salary_structure_id
        ).first()
        
        if db_salary:
            update_data = salary.model_dump(exclude_none=True)
            
            # Set ModifiedOn timestamp
            update_data['ModifiedOn'] = datetime.utcnow()
            
            # Update fields
            for key, value in update_data.items():
                setattr(db_salary, key, value)
            
            # Calculate and update totals
            totals = EmployeeSalaryStructureService.calculate_salary_totals(db_salary)
            db_salary.GROSSEARNINGS = totals["GROSSEARNINGS"]
            db_salary.GROSSDEDUCTIONS = totals["GROSSDEDUCTIONS"]
            
            db.commit()
            db.refresh(db_salary)
        
        return db_salary
    
    @staticmethod
    def check_salary_structure_exists(
        db: Session, 
        employee_id: int
    ) -> Dict[str, Any]:
        """Check if salary structure exists for employee"""
        salary = db.query(EmployeeSalaryStructure).filter(
            EmployeeSalaryStructure.EmployeeId == employee_id,
            EmployeeSalaryStructure.IsActive == True
        ).first()
        
        return {
            "exists": salary is not None,
            "employee_salary_structure_id": salary.EmployeeSalaryStructureId if salary else None
        }
    
    @staticmethod
    def get_salary_breakdown(
        db: Session, 
        employee_salary_structure_id: int
    ) -> Dict[str, Any]:
        """Get detailed salary breakdown"""
        salary = db.query(EmployeeSalaryStructure).filter(
            EmployeeSalaryStructure.EmployeeSalaryStructureId == employee_salary_structure_id
        ).first()
        
        if not salary:
            return {"error": "Salary structure not found"}
        
        totals = EmployeeSalaryStructureService.calculate_salary_totals(salary)
        gross_earnings = totals["GROSSEARNINGS"]
        
        # Calculate percentages
        earnings = {
            "BASIC": salary.BASIC or 0,
            "HRA": salary.HRA or 0,
            "CONVEYANCE": salary.CONVEYANCE or 0,
            "MEDICALALLOWANCE": salary.MEDICALALLOWANCE or 0,
            "SPECIALALLOWANCE": salary.SPECIALALLOWANCE or 0,
            "SPECIALBONUS": salary.SPECIALBONUS or 0,
            "STATUTORYBONUS": salary.STATUTORYBONUS or 0,
            "OTHERS": salary.OTHERS or 0
        }
        
        deductions = {
            "PF": salary.PF or 0,
            "ESIC": salary.ESIC or 0,
            "PROFESSIONALTAX": salary.PROFESSIONALTAX or 0,
            "GroupHealthInsurance": salary.GroupHealthInsurance or 0
        }
        
        # Calculate percentages
        earnings_percentages = {
            key: float((value / gross_earnings) * 100) if gross_earnings > 0 else 0
            for key, value in earnings.items()
        }
        
        deductions_percentages = {
            key: float((value / gross_earnings) * 100) if gross_earnings > 0 else 0
            for key, value in deductions.items()
        }
        
        return {
            "earnings": {k: Decimal(str(v)) for k, v in earnings.items()},
            "deductions": {k: Decimal(str(v)) for k, v in deductions.items()},
            "totals": totals,
            "percentages": {
                "earnings": earnings_percentages,
                "deductions": deductions_percentages
            }
        }
    
    @staticmethod
    def get_salary_statistics(db: Session) -> Dict[str, Any]:
        """Get salary statistics"""
        # Basic statistics
        total_employees = db.query(func.count(EmployeeSalaryStructure.EmployeeSalaryStructureId)).filter(
            EmployeeSalaryStructure.IsActive == True
        ).scalar()
        
        # Average values
        avg_basic = db.query(func.avg(EmployeeSalaryStructure.BASIC)).filter(
            EmployeeSalaryStructure.IsActive == True
        ).scalar() or 0
        
        avg_gross_earnings = db.query(func.avg(EmployeeSalaryStructure.GROSSEARNINGS)).filter(
            EmployeeSalaryStructure.IsActive == True
        ).scalar() or 0
        
        # Calculate average net take-home
        avg_net_query = db.query(
            func.avg(
                EmployeeSalaryStructure.GROSSEARNINGS - EmployeeSalaryStructure.GROSSDEDUCTIONS
            )
        ).filter(
            EmployeeSalaryStructure.IsActive == True
        ).scalar() or 0
        
        # Highest and lowest salaries
        highest_salary = db.query(
            func.max(EmployeeSalaryStructure.GROSSEARNINGS)
        ).filter(
            EmployeeSalaryStructure.IsActive == True
        ).scalar() or 0
        
        lowest_salary = db.query(
            func.min(EmployeeSalaryStructure.GROSSEARNINGS)
        ).filter(
            EmployeeSalaryStructure.IsActive == True,
            EmployeeSalaryStructure.GROSSEARNINGS > 0
        ).scalar() or 0
        
        # Salary distribution
        salary_ranges = [
            (0, 30000, "Below 30k"),
            (30000, 50000, "30k - 50k"),
            (50000, 80000, "50k - 80k"),
            (80000, 120000, "80k - 1.2L"),
            (120000, 200000, "1.2L - 2L"),
            (200000, 999999999, "Above 2L")
        ]
        
        distribution = {}
        for min_val, max_val, label in salary_ranges:
            count = db.query(func.count(EmployeeSalaryStructure.EmployeeSalaryStructureId)).filter(
                EmployeeSalaryStructure.IsActive == True,
                EmployeeSalaryStructure.GROSSEARNINGS >= min_val,
                EmployeeSalaryStructure.GROSSEARNINGS < max_val
            ).scalar()
            distribution[label] = count
        
        return {
            "total_employees": total_employees,
            "average_basic": Decimal(str(avg_basic)),
            "average_gross_earnings": Decimal(str(avg_gross_earnings)),
            "average_net_takehome": Decimal(str(avg_net_query)),
            "highest_salary": Decimal(str(highest_salary)),
            "lowest_salary": Decimal(str(lowest_salary)),
            "salary_distribution": distribution
        }
    
    @staticmethod
    def get_salary_comparison_report(db: Session, department_id: Optional[int] = None) -> Dict[str, Any]:
        """Get salary comparison report"""
        query = db.query(
            EmployeeSalaryStructure,
            Employee
        ).join(
            Employee, EmployeeSalaryStructure.EmployeeId == Employee.EmployeeId
        ).filter(
            EmployeeSalaryStructure.IsActive == True
        )
        
        if department_id:
            query = query.filter(Employee.DepartmentId == department_id)
        
        results = query.all()
        
        # Group by designation
        by_designation = {}
        for salary, employee in results:
            designation = "Unknown"
            if hasattr(employee, 'Designation') and employee.Designation:
                designation = employee.Designation
            elif hasattr(employee, 'designation') and employee.designation:
                designation = employee.designation
            
            if designation not in by_designation:
                by_designation[designation] = {
                    "count": 0,
                    "total_basic": Decimal('0'),
                    "total_gross": Decimal('0'),
                    "salaries": []
                }
            
            totals = EmployeeSalaryStructureService.calculate_salary_totals(salary)
            by_designation[designation]["count"] += 1
            by_designation[designation]["total_basic"] += (salary.BASIC or 0)
            by_designation[designation]["total_gross"] += totals["GROSSEARNINGS"]
            by_designation[designation]["salaries"].append({
                "employee_id": employee.EmployeeId,
                "employee_name": f"{employee.FirstName} {employee.LastName}".strip(),
                "basic": salary.BASIC or 0,
                "gross": totals["GROSSEARNINGS"],
                "net": totals["NETTAKEHOME"]
            })
        
        # Calculate averages
        for designation in by_designation:
            data = by_designation[designation]
            if data["count"] > 0:
                data["avg_basic"] = data["total_basic"] / data["count"]
                data["avg_gross"] = data["total_gross"] / data["count"]
        
        return {
            "total_employees": len(results),
            "by_designation": by_designation
        }