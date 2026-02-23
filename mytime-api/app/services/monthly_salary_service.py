from sqlalchemy.orm import Session, selectinload
from typing import Optional, List, Union, Dict, Any, Tuple
from sqlalchemy import and_

from app.models.monthly_salary import MonthlySalary
from app.models.employee import Employee
from app.models.employee_salary_structure import EmployeeSalaryStructure
from app.models.employee_salary import EmployeeSalary
from app.schemas.monthly_salary_schemas import (
    MonthlySalaryCreate, 
    MonthlySalaryUpdate
)
from app.utils.month_converter import MonthToYearConverter
from app.utils.indian_salary_converter import IndianSalaryConverter
import math

class MonthlySalaryService:
    @staticmethod
    def fetch_monthly_salary(db: Session, salary_id: int) -> Optional[MonthlySalary]:
        """Get monthly salary by ID"""
        return db.query(MonthlySalary).filter(MonthlySalary.MonthlySalaryId == salary_id).first()
    
    @staticmethod
    def fetch_all_monthly_salaries(db: Session) -> List[MonthlySalary]:
        """Get all monthly salaries"""
        return db.query(MonthlySalary).all()

    @staticmethod
    def fetch_all_monthly_salaries_with_employees(db: Session) -> List[MonthlySalary]:
        """Get all monthly salaries with their employee salaries eagerly loaded"""
        return (
            db.query(MonthlySalary)
            .options(selectinload(MonthlySalary.employee_salaries))
            .all()
        )

    @staticmethod
    def fetch_monthly_salary_with_employees(
        db: Session,
        salary_id: int,
        is_active_employees: Optional[bool] = None,
    ) -> Optional[MonthlySalary]:
        """
        Get a single monthly salary with its employee salaries eagerly loaded.
        Optionally filter the nested employee salaries by IsActive status.

        Returns:
            MonthlySalary ORM object (with .employee_salaries populated)
            or None if not found
        """
        record = (
            db.query(MonthlySalary)
            .options(selectinload(MonthlySalary.employee_salaries))
            .filter(MonthlySalary.MonthlySalaryId == salary_id)
            .first()
        )

        if record is None:
            return None

        # Post-filter nested employee salaries when requested
        if is_active_employees is not None:
            record.employee_salaries = [
                emp for emp in record.employee_salaries
                if emp.IsActive == is_active_employees
            ]

        return record

    @staticmethod
    def create_monthly_salary(db: Session, salary_data: MonthlySalaryCreate) -> MonthlySalary:
        """Insert new monthly salary record"""
        salary_dict = salary_data.model_dump(exclude_unset=True)
        salary = MonthlySalary(**salary_dict)
        db.add(salary)
        db.commit()
        db.refresh(salary)
        return salary
    
    @staticmethod
    def update_monthly_salary(db: Session, salary_id: int, salary_data: MonthlySalaryUpdate) -> MonthlySalary:
        """Update existing monthly salary record"""
        salary = db.query(MonthlySalary).filter(MonthlySalary.MonthlySalaryId == salary_id).first()
        if not salary:
            raise ValueError(f"Monthly salary record with ID {salary_id} not found for update")
        
        update_data = salary_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(salary, field, value)
        
        db.commit()
        db.refresh(salary)
        return salary
    
    @staticmethod
    def insert_or_update_monthly_salary(
        db: Session, 
        salary_data: Union[MonthlySalaryCreate, Dict[str, Any]], 
        salary_id: Optional[int] = None
    ) -> MonthlySalary:
        """Insert or update monthly salary record"""
        if isinstance(salary_data, dict):
            if salary_id:
                salary_data = MonthlySalaryUpdate(**salary_data)
            else:
                salary_data = MonthlySalaryCreate(**salary_data)
        
        if salary_id:
            return MonthlySalaryService.update_monthly_salary(db, salary_id, salary_data)
        else:
            return MonthlySalaryService.create_monthly_salary(db, salary_data)
    
    @staticmethod
    def delete_monthly_salary(db: Session, salary_id: int) -> bool:
        """Delete monthly salary record by ID"""
        salary = db.query(MonthlySalary).filter(MonthlySalary.MonthlySalaryId == salary_id).first()
        if not salary:
            raise ValueError(f"Monthly salary record with ID {salary_id} not found for deletion")
        db.delete(salary)
        db.commit()
        return True
    
    @staticmethod
    def publish_monthly_salary(db: Session, monthly_salary: MonthlySalary) -> bool:
        """
        Publish monthly salary for all active employees
        Equivalent to C# PublishMonthlySalary method
        """
        db.add(monthly_salary)
        db.flush()
        
        active_employees = db.query(Employee.EmployeeId).filter(
            Employee.IsActive == True
        ).all()
        active_employee_ids = [emp.EmployeeId for emp in active_employees]
        
        if active_employee_ids:
            salary_structures = db.query(EmployeeSalaryStructure).filter(
                EmployeeSalaryStructure.EmployeeId.in_(active_employee_ids),
                EmployeeSalaryStructure.IsActive == True
            ).all()
            
            existing_salaries = db.query(EmployeeSalary).filter(
                EmployeeSalary.EmployeeId.in_(active_employee_ids)
            ).all()
            
            employee_salaries: List[EmployeeSalary] = []
            
            standard_days = MonthToYearConverter.get_days_in_month(
                monthly_salary.SalaryMonth, 
                int(monthly_salary.SalaryYear)
            )
            
            adjusted_month = MonthToYearConverter.get_adjusted_month_number(
                monthly_salary.SalaryMonth,
                int(monthly_salary.SalaryYear)
            )
            
            lop_days = 0
            
            for structure in salary_structures:
                employee_salary = EmployeeSalary()
                employee_salary.MonthlySalaryId = monthly_salary.MonthlySalaryId
                employee_salary.EmployeeId = structure.EmployeeId
                employee_salary.Title = monthly_salary.Title
                employee_salary.SalaryMonth = monthly_salary.SalaryMonth
                employee_salary.SalaryYear = monthly_salary.SalaryYear
                employee_salary.LOCATION = monthly_salary.Location
                employee_salary.STDDAYS = standard_days
                employee_salary.LOPDAYS = lop_days
                employee_salary.WRKDAYS = standard_days
                
                max_employee_salary = None
                matching_salaries = [
                    s for s in existing_salaries 
                    if s.EmployeeId == structure.EmployeeId 
                    and MonthlySalaryService.is_in_financial_year(
                        s.SalaryMonth, 
                        s.SalaryYear, 
                        monthly_salary.SalaryMonth, 
                        monthly_salary.SalaryYear
                    )
                ]
                if matching_salaries:
                    max_employee_salary = max(
                        matching_salaries, 
                        key=lambda x: x.Earning_YTD_Basic or 0
                    )
                
                if max_employee_salary is None:
                    MonthlySalaryService._set_first_time_salaries(employee_salary, structure, adjusted_month)
                else:
                    MonthlySalaryService._set_subsequent_salaries(employee_salary, structure, max_employee_salary)
                
                net_salary = (structure.GROSSEARNINGS or 0) - (structure.GROSSDEDUCTIONS or 0)
                
                employee_salary.INWords = IndianSalaryConverter.convert_to_words(net_salary)
                
                employee_salary.CreatedBy = monthly_salary.CreatedBy
                employee_salary.ModifiedBy = monthly_salary.ModifiedBy
                employee_salary.CreatedOn = monthly_salary.CreatedOn
                employee_salary.ModifiedOn = monthly_salary.ModifiedOn
                employee_salary.IsActive = True
                
                employee_salaries.append(employee_salary)
            
            if employee_salaries:
                db.add_all(employee_salaries)
            
            db.commit()
            return True
        
        return False
    
    @staticmethod
    def _set_first_time_salaries(
        employee_salary: EmployeeSalary, 
        structure: EmployeeSalaryStructure, 
        adjusted_month: int
    ) -> None:
        employee_salary.Earning_Monthly_Basic = structure.BASIC
        employee_salary.Earning_YTD_Basic = (structure.BASIC or 0) * adjusted_month
        employee_salary.Earning_Montly_HRA = structure.HRA
        employee_salary.Earning_YTD_HRA = (structure.HRA or 0) * adjusted_month
        employee_salary.Earning_Montly_CONVEYANCE = structure.CONVEYANCE
        employee_salary.Earning_YTD_CONVEYANCE = (structure.CONVEYANCE or 0) * adjusted_month
        employee_salary.Earning_Montly_MEDICALALLOWANCE = structure.MEDICALALLOWANCE
        employee_salary.Earning_YTD_MEDICALALLOWANCE = (structure.MEDICALALLOWANCE or 0) * adjusted_month
        employee_salary.Earning_Montly_SPECIALALLOWANCE = structure.SPECIALALLOWANCE
        employee_salary.Earning_YTD_SPECIALALLOWANCE = (structure.SPECIALALLOWANCE or 0) * adjusted_month
        employee_salary.Earning_Montly_STATUTORYBONUS = structure.STATUTORYBONUS
        employee_salary.Earning_YTD_STATUTORYBONUS = (structure.STATUTORYBONUS or 0) * adjusted_month
        employee_salary.Earning_Montly_OTHERS = structure.OTHERS
        employee_salary.Earning_YTD_OTHERS = (structure.OTHERS or 0) * adjusted_month
        employee_salary.Earning_Montly_GROSSEARNINGS = structure.GROSSEARNINGS
        employee_salary.Earning_YTD_GROSSEARNINGS = (structure.GROSSEARNINGS or 0) * adjusted_month
        employee_salary.Deduction_Montly_ProvidentFund = structure.PF
        employee_salary.Deduction_YTD_ProvidentFund = (structure.PF or 0) * adjusted_month
        employee_salary.Deduction_Montly_PROFESSIONALTAX = structure.PROFESSIONALTAX
        employee_salary.Deduction_YTD_PROFESSIONALTAX = (structure.PROFESSIONALTAX or 0) * adjusted_month
        employee_salary.Deduction_Montly_GroupHealthInsurance = structure.GroupHealthInsurance
        employee_salary.Deduction_YTD_GroupHealthInsurance = (structure.GroupHealthInsurance or 0) * adjusted_month
        employee_salary.Deduction_Montly_OTHERS = 0
        employee_salary.Deduction_YTD_OTHERS = 0
        employee_salary.Deduction_Montly_GROSSSDeduction = structure.GROSSDEDUCTIONS
        employee_salary.Deduction_YTD_GROSSSDeduction = (structure.GROSSDEDUCTIONS or 0) * adjusted_month
        employee_salary.NETTRANSFER = (structure.GROSSEARNINGS or 0) - (structure.GROSSDEDUCTIONS or 0)
        employee_salary.NETPAY = (structure.GROSSEARNINGS or 0) - (structure.GROSSDEDUCTIONS or 0)
    
    @staticmethod
    def _set_subsequent_salaries(
        employee_salary: EmployeeSalary, 
        structure: EmployeeSalaryStructure, 
        max_salary: EmployeeSalary
    ) -> None:
        employee_salary.Earning_Monthly_Basic = structure.BASIC
        employee_salary.Earning_YTD_Basic = (structure.BASIC or 0) + (max_salary.Earning_YTD_Basic or 0)
        employee_salary.Earning_Montly_HRA = structure.HRA
        employee_salary.Earning_YTD_HRA = (structure.HRA or 0) + (max_salary.Earning_YTD_HRA or 0)
        employee_salary.Earning_Montly_CONVEYANCE = structure.CONVEYANCE
        employee_salary.Earning_YTD_CONVEYANCE = (structure.CONVEYANCE or 0) + (max_salary.Earning_YTD_CONVEYANCE or 0)
        employee_salary.Earning_Montly_MEDICALALLOWANCE = structure.MEDICALALLOWANCE
        employee_salary.Earning_YTD_MEDICALALLOWANCE = (structure.MEDICALALLOWANCE or 0) + (max_salary.Earning_YTD_MEDICALALLOWANCE or 0)
        employee_salary.Earning_Montly_SPECIALALLOWANCE = structure.SPECIALALLOWANCE
        employee_salary.Earning_YTD_SPECIALALLOWANCE = (structure.SPECIALALLOWANCE or 0) + (max_salary.Earning_YTD_SPECIALALLOWANCE or 0)
        employee_salary.Earning_Montly_STATUTORYBONUS = structure.STATUTORYBONUS
        employee_salary.Earning_YTD_STATUTORYBONUS = (structure.STATUTORYBONUS or 0) + (max_salary.Earning_YTD_STATUTORYBONUS or 0)
        employee_salary.Earning_Montly_OTHERS = structure.OTHERS
        employee_salary.Earning_YTD_OTHERS = (structure.OTHERS or 0) + (max_salary.Earning_YTD_OTHERS or 0)
        employee_salary.Earning_Montly_GROSSEARNINGS = structure.GROSSEARNINGS
        employee_salary.Earning_YTD_GROSSEARNINGS = (structure.GROSSEARNINGS or 0) + (max_salary.Earning_YTD_GROSSEARNINGS or 0)
        employee_salary.Deduction_Montly_ProvidentFund = structure.PF
        employee_salary.Deduction_YTD_ProvidentFund = (structure.PF or 0) + (max_salary.Deduction_YTD_ProvidentFund or 0)
        employee_salary.Deduction_Montly_PROFESSIONALTAX = structure.PROFESSIONALTAX
        employee_salary.Deduction_YTD_PROFESSIONALTAX = (structure.PROFESSIONALTAX or 0) + (max_salary.Deduction_YTD_PROFESSIONALTAX or 0)
        employee_salary.Deduction_Montly_GroupHealthInsurance = structure.GroupHealthInsurance
        employee_salary.Deduction_YTD_GroupHealthInsurance = (structure.GroupHealthInsurance or 0) + (max_salary.Deduction_YTD_GroupHealthInsurance or 0)
        employee_salary.Deduction_Montly_OTHERS = 0
        employee_salary.Deduction_YTD_OTHERS = (max_salary.Deduction_YTD_OTHERS or 0) + 0
        employee_salary.Deduction_Montly_GROSSSDeduction = structure.GROSSDEDUCTIONS
        employee_salary.Deduction_YTD_GROSSSDeduction = (structure.GROSSDEDUCTIONS or 0) + (max_salary.Deduction_YTD_GROSSSDeduction or 0)
        employee_salary.NETTRANSFER = (structure.GROSSEARNINGS or 0) - (structure.GROSSDEDUCTIONS or 0)
        employee_salary.NETPAY = (structure.GROSSEARNINGS or 0) - (structure.GROSSDEDUCTIONS or 0)
    
    @staticmethod
    def is_in_financial_year(
        salary_month: str, 
        salary_year: str, 
        target_month: str, 
        target_year: str
    ) -> bool:
        month_order = {
            'January': 1, 'February': 2, 'March': 3, 'April': 4,
            'May': 5, 'June': 6, 'July': 7, 'August': 8,
            'September': 9, 'October': 10, 'November': 11, 'December': 12
        }
        salary_month_num = month_order.get(salary_month, 0)
        target_month_num = month_order.get(target_month, 0)
        salary_year_int = int(salary_year)
        target_year_int = int(target_year)
        if target_month_num >= 4:
            if salary_month_num >= 4:
                return salary_year_int == target_year_int
            else:
                return salary_year_int == target_year_int + 1
        else:
            if salary_month_num >= 4:
                return salary_year_int == target_year_int - 1
            else:
                return salary_year_int == target_year_int