from sqlalchemy.orm import Session, selectinload
from typing import Optional, List, Union, Dict, Any, Tuple
from sqlalchemy import and_
import logging
from datetime import datetime

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

logger = logging.getLogger(__name__)

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
        logger.info(f"Created monthly salary with ID: {salary.MonthlySalaryId}")
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
        logger.info(f"Updated monthly salary with ID: {salary_id}, fields: {list(update_data.keys())}")
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
        logger.info(f"Deleted monthly salary with ID: {salary_id}")
        return True
    
    @staticmethod
    def is_april_month(month: str) -> bool:
        """Check if given month is April"""
        return month.lower() == 'april'
    
    @staticmethod
    def get_financial_year(month: str, year: int) -> Tuple[int, int]:
        """
        Get financial year for a given month and year
        Returns: (financial_year_start, financial_year_end)
        Example: April 2024 -> (2024, 2025)
                May 2024 -> (2024, 2025)
                March 2024 -> (2023, 2024)
        """
        month_order = {
            'January': 1, 'February': 2, 'March': 3, 'April': 4,
            'May': 5, 'June': 6, 'July': 7, 'August': 8,
            'September': 9, 'October': 10, 'November': 11, 'December': 12
        }
        month_num = month_order.get(month, 0)
        
        if month_num >= 4:  # April to December
            return (year, year + 1)
        else:  # January to March
            return (year - 1, year)
    
    @staticmethod
    def get_previous_salaries_in_current_financial_year(
        db: Session,
        employee_id: int,
        current_month: str,
        current_year: str,
        current_monthly_salary_id: int
    ) -> List[EmployeeSalary]:
        """
        Get all previous salaries for an employee in the current financial year
        (from April to current month)
        """
        current_year_int = int(current_year)
        month_order = {
            'January': 1, 'February': 2, 'March': 3, 'April': 4,
            'May': 5, 'June': 6, 'July': 7, 'August': 8,
            'September': 9, 'October': 10, 'November': 11, 'December': 12
        }
        current_month_num = month_order.get(current_month, 0)
        
        # Get financial year for current month
        fy_start, fy_end = MonthlySalaryService.get_financial_year(current_month, current_year_int)
        
        logger.info(f"Finding previous salaries for employee {employee_id} in financial year {fy_start}-{fy_end}")
        
        # Get all salaries for this employee (excluding current one)
        all_employee_salaries = db.query(EmployeeSalary).filter(
            EmployeeSalary.EmployeeId == employee_id,
            EmployeeSalary.MonthlySalaryId != current_monthly_salary_id,
            EmployeeSalary.IsActive == True
        ).all()
        
        # Filter to only those in the current financial year
        previous_salaries = []
        
        for sal in all_employee_salaries:
            sal_year = int(sal.SalaryYear)
            sal_month_num = month_order.get(sal.SalaryMonth, 0)
            
            # Check if this salary is in the current financial year
            if sal_month_num >= 4:  # April to December
                in_fy = (sal_year == fy_start)
            else:  # January to March
                in_fy = (sal_year == fy_end)
            
            if in_fy:
                # Also ensure it's before current month
                sal_is_before = False
                if sal_year < current_year_int:
                    sal_is_before = True
                elif sal_year == current_year_int and sal_month_num < current_month_num:
                    sal_is_before = True
                elif sal_year < current_year_int and sal_month_num >= 4:
                    # Special case: previous year's April-December is before current year's Jan-March
                    if current_month_num < 4:
                        sal_is_before = True
                
                if sal_is_before:
                    previous_salaries.append(sal)
                    logger.info(f"Found previous salary: {sal.SalaryMonth} {sal.SalaryYear}")
        
        # Sort by date (oldest first)
        previous_salaries.sort(key=lambda x: (
            int(x.SalaryYear),
            month_order.get(x.SalaryMonth, 0)
        ))
        
        return previous_salaries
    
    @staticmethod
    def publish_monthly_salary(db: Session, monthly_salary: MonthlySalary) -> Tuple[bool, int]:
        """
        Publish monthly salary for all active employees
        Returns: (success, number_of_employees_processed)
        """
        logger.info(f"Starting publish for monthly salary ID: {monthly_salary.MonthlySalaryId}, Month: {monthly_salary.SalaryMonth} {monthly_salary.SalaryYear}")
        
        # Check if monthly salary already has employee salaries
        existing_employee_salaries = db.query(EmployeeSalary).filter(
            EmployeeSalary.MonthlySalaryId == monthly_salary.MonthlySalaryId
        ).all()
        
        is_update = len(existing_employee_salaries) > 0
        if is_update:
            logger.info(f"Monthly salary {monthly_salary.MonthlySalaryId} is being updated with {len(existing_employee_salaries)} existing employee records")
        
        # Get active employees
        active_employees = db.query(Employee.EmployeeId).filter(
            Employee.IsActive == True
        ).all()
        active_employee_ids = [emp.EmployeeId for emp in active_employees]
        
        if not active_employee_ids:
            logger.warning(f"No active employees found for monthly salary {monthly_salary.MonthlySalaryId}")
            return False, 0
        
        # Get salary structures for active employees
        salary_structures = db.query(EmployeeSalaryStructure).filter(
            EmployeeSalaryStructure.EmployeeId.in_(active_employee_ids),
            EmployeeSalaryStructure.IsActive == True
        ).all()
        
        if not salary_structures:
            logger.warning(f"No salary structures found for active employees")
            return False, 0
        
        # Calculate standard days
        standard_days = MonthToYearConverter.get_days_in_month(
            monthly_salary.SalaryMonth, 
            int(monthly_salary.SalaryYear)
        )
        
        lop_days = 0
        
        # Check if this is April (new financial year)
        is_april = MonthlySalaryService.is_april_month(monthly_salary.SalaryMonth)
        if is_april:
            logger.info(f"Processing April salary - starting new financial year")
        
        # Get financial year for current month
        current_year_int = int(monthly_salary.SalaryYear)
        fy_start, fy_end = MonthlySalaryService.get_financial_year(monthly_salary.SalaryMonth, current_year_int)
        logger.info(f"Current financial year: {fy_start}-{fy_end}")
        
        # Process each employee
        employee_salaries_to_add = []
        employee_salaries_to_update = []
        
        for structure in salary_structures:
            # Check if employee salary already exists for this monthly salary
            existing_employee_salary = next(
                (es for es in existing_employee_salaries if es.EmployeeId == structure.EmployeeId),
                None
            )
            
            if existing_employee_salary and is_update:
                # Update existing record
                employee_salary = existing_employee_salary
                MonthlySalaryService._update_employee_salary_from_monthly(
                    employee_salary, monthly_salary, standard_days, lop_days
                )
                employee_salaries_to_update.append(employee_salary)
                logger.info(f"Updating existing salary for employee {structure.EmployeeId}")
            else:
                # Create new record
                logger.info(f"Creating new salary for employee {structure.EmployeeId}")
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
                
                # Check if this is April - RESET YTD
                if is_april:
                    logger.info(f"April month detected for employee {structure.EmployeeId} - RESETTING YTD")
                    MonthlySalaryService._set_first_month_of_financial_year(employee_salary, structure)
                else:
                    # Find previous salaries in the SAME FINANCIAL YEAR only
                    previous_salaries = MonthlySalaryService.get_previous_salaries_in_current_financial_year(
                        db, 
                        structure.EmployeeId,
                        monthly_salary.SalaryMonth,
                        monthly_salary.SalaryYear,
                        monthly_salary.MonthlySalaryId
                    )
                    
                    if not previous_salaries:
                        # First salary in this financial year (but not April)
                        logger.info(f"First salary in financial year {fy_start}-{fy_end} for employee {structure.EmployeeId} - starting fresh")
                        MonthlySalaryService._set_first_month_of_financial_year(employee_salary, structure)
                    else:
                        # Has previous salaries in same financial year - accumulate
                        # Find the latest previous salary to get correct YTD
                        latest_previous = previous_salaries[-1]  # Last one after sorting
                        logger.info(f"Found {len(previous_salaries)} previous salaries for employee {structure.EmployeeId} in same financial year")
                        logger.info(f"Latest previous salary: {latest_previous.SalaryMonth} {latest_previous.SalaryYear} with YTD Basic: {latest_previous.Earning_YTD_Basic}")
                        MonthlySalaryService._set_subsequent_salaries(employee_salary, structure, latest_previous)
                
                net_salary = (structure.GROSSEARNINGS or 0) - (structure.GROSSDEDUCTIONS or 0)
                employee_salary.INWords = IndianSalaryConverter.convert_to_words(net_salary)
                
                employee_salary.CreatedBy = monthly_salary.CreatedBy
                employee_salary.ModifiedBy = monthly_salary.ModifiedBy
                employee_salary.CreatedOn = monthly_salary.CreatedOn
                employee_salary.ModifiedOn = monthly_salary.ModifiedOn
                employee_salary.IsActive = True
                
                employee_salaries_to_add.append(employee_salary)
                
                # Log the values being set
                logger.info(f"Employee {structure.EmployeeId} - Monthly Basic: {employee_salary.Earning_Monthly_Basic}, YTD Basic: {employee_salary.Earning_YTD_Basic}")
        
        # Bulk operations
        if employee_salaries_to_add:
            db.add_all(employee_salaries_to_add)
            logger.info(f"Added {len(employee_salaries_to_add)} new employee salaries")
        
        if employee_salaries_to_update:
            logger.info(f"Updated {len(employee_salaries_to_update)} existing employee salaries")
        
        db.commit()
        
        total_processed = len(employee_salaries_to_add) + len(employee_salaries_to_update)
        logger.info(f"Successfully published monthly salary {monthly_salary.MonthlySalaryId} for {total_processed} employees")
        
        return True, total_processed
    
    @staticmethod
    def _update_employee_salary_from_monthly(
        employee_salary: EmployeeSalary,
        monthly_salary: MonthlySalary,
        standard_days: int,
        lop_days: int
    ) -> None:
        """Update employee salary with monthly salary changes"""
        employee_salary.Title = monthly_salary.Title
        employee_salary.SalaryMonth = monthly_salary.SalaryMonth
        employee_salary.SalaryYear = monthly_salary.SalaryYear
        employee_salary.LOCATION = monthly_salary.Location
        employee_salary.STDDAYS = standard_days
        employee_salary.LOPDAYS = lop_days
        employee_salary.WRKDAYS = standard_days
        employee_salary.ModifiedOn = monthly_salary.ModifiedOn
        employee_salary.ModifiedBy = monthly_salary.ModifiedBy
    
    @staticmethod
    def check_if_reprocessing_needed(
        old_salary: MonthlySalary,
        new_data: MonthlySalaryUpdate
    ) -> bool:
        """Check if employee salaries need reprocessing based on changed fields"""
        update_data = new_data.model_dump(exclude_unset=True)
        
        # Fields that impact employee salaries
        employee_impacting_fields = {
            'Title', 'SalaryMonth', 'SalaryYear', 'Location', 
            'StdDays', 'WrkDays', 'LopDays'
        }
        
        changed_fields = set(update_data.keys())
        needs_reprocessing = bool(changed_fields & employee_impacting_fields)
        
        if needs_reprocessing:
            logger.info(f"Reprocessing needed due to changes in: {changed_fields & employee_impacting_fields}")
        
        return needs_reprocessing
    
    @staticmethod
    def _set_first_month_of_financial_year(
        employee_salary: EmployeeSalary, 
        structure: EmployeeSalaryStructure
    ) -> None:
        """
        Set salaries for first month of financial year (April or first month after April)
        YTD equals monthly amount (no accumulation from previous financial year)
        """
        employee_salary.Earning_Monthly_Basic = structure.BASIC
        employee_salary.Earning_YTD_Basic = structure.BASIC  # Just this month
        
        employee_salary.Earning_Montly_HRA = structure.HRA
        employee_salary.Earning_YTD_HRA = structure.HRA
        
        employee_salary.Earning_Montly_CONVEYANCE = structure.CONVEYANCE
        employee_salary.Earning_YTD_CONVEYANCE = structure.CONVEYANCE
        
        employee_salary.Earning_Montly_MEDICALALLOWANCE = structure.MEDICALALLOWANCE
        employee_salary.Earning_YTD_MEDICALALLOWANCE = structure.MEDICALALLOWANCE
        
        employee_salary.Earning_Montly_SPECIALALLOWANCE = structure.SPECIALALLOWANCE
        employee_salary.Earning_YTD_SPECIALALLOWANCE = structure.SPECIALALLOWANCE
        
        employee_salary.Earning_Montly_STATUTORYBONUS = structure.STATUTORYBONUS
        employee_salary.Earning_YTD_STATUTORYBONUS = structure.STATUTORYBONUS
        
        employee_salary.Earning_Montly_OTHERS = structure.OTHERS
        employee_salary.Earning_YTD_OTHERS = structure.OTHERS
        
        employee_salary.Earning_Montly_GROSSEARNINGS = structure.GROSSEARNINGS
        employee_salary.Earning_YTD_GROSSEARNINGS = structure.GROSSEARNINGS
        
        employee_salary.Deduction_Montly_ProvidentFund = structure.PF
        employee_salary.Deduction_YTD_ProvidentFund = structure.PF
        
        employee_salary.Deduction_Montly_PROFESSIONALTAX = structure.PROFESSIONALTAX
        employee_salary.Deduction_YTD_PROFESSIONALTAX = structure.PROFESSIONALTAX
        
        employee_salary.Deduction_Montly_GroupHealthInsurance = structure.GroupHealthInsurance
        employee_salary.Deduction_YTD_GroupHealthInsurance = structure.GroupHealthInsurance
        
        employee_salary.Deduction_Montly_OTHERS = 0
        employee_salary.Deduction_YTD_OTHERS = 0
        
        employee_salary.Deduction_Montly_GROSSSDeduction = structure.GROSSDEDUCTIONS
        employee_salary.Deduction_YTD_GROSSSDeduction = structure.GROSSDEDUCTIONS
        
        employee_salary.NETTRANSFER = (structure.GROSSEARNINGS or 0) - (structure.GROSSDEDUCTIONS or 0)
        employee_salary.NETPAY = (structure.GROSSEARNINGS or 0) - (structure.GROSSDEDUCTIONS or 0)
    
    @staticmethod
    def _set_subsequent_salaries(
        employee_salary: EmployeeSalary, 
        structure: EmployeeSalaryStructure, 
        previous_salary: EmployeeSalary
    ) -> None:
        """
        Set salaries for subsequent months in the same financial year
        Add current month to previous YTD
        """
        employee_salary.Earning_Monthly_Basic = structure.BASIC
        employee_salary.Earning_YTD_Basic = (structure.BASIC or 0) + (previous_salary.Earning_YTD_Basic or 0)
        
        employee_salary.Earning_Montly_HRA = structure.HRA
        employee_salary.Earning_YTD_HRA = (structure.HRA or 0) + (previous_salary.Earning_YTD_HRA or 0)
        
        employee_salary.Earning_Montly_CONVEYANCE = structure.CONVEYANCE
        employee_salary.Earning_YTD_CONVEYANCE = (structure.CONVEYANCE or 0) + (previous_salary.Earning_YTD_CONVEYANCE or 0)
        
        employee_salary.Earning_Montly_MEDICALALLOWANCE = structure.MEDICALALLOWANCE
        employee_salary.Earning_YTD_MEDICALALLOWANCE = (structure.MEDICALALLOWANCE or 0) + (previous_salary.Earning_YTD_MEDICALALLOWANCE or 0)
        
        employee_salary.Earning_Montly_SPECIALALLOWANCE = structure.SPECIALALLOWANCE
        employee_salary.Earning_YTD_SPECIALALLOWANCE = (structure.SPECIALALLOWANCE or 0) + (previous_salary.Earning_YTD_SPECIALALLOWANCE or 0)
        
        employee_salary.Earning_Montly_STATUTORYBONUS = structure.STATUTORYBONUS
        employee_salary.Earning_YTD_STATUTORYBONUS = (structure.STATUTORYBONUS or 0) + (previous_salary.Earning_YTD_STATUTORYBONUS or 0)
        
        employee_salary.Earning_Montly_OTHERS = structure.OTHERS
        employee_salary.Earning_YTD_OTHERS = (structure.OTHERS or 0) + (previous_salary.Earning_YTD_OTHERS or 0)
        
        employee_salary.Earning_Montly_GROSSEARNINGS = structure.GROSSEARNINGS
        employee_salary.Earning_YTD_GROSSEARNINGS = (structure.GROSSEARNINGS or 0) + (previous_salary.Earning_YTD_GROSSEARNINGS or 0)
        
        employee_salary.Deduction_Montly_ProvidentFund = structure.PF
        employee_salary.Deduction_YTD_ProvidentFund = (structure.PF or 0) + (previous_salary.Deduction_YTD_ProvidentFund or 0)
        
        employee_salary.Deduction_Montly_PROFESSIONALTAX = structure.PROFESSIONALTAX
        employee_salary.Deduction_YTD_PROFESSIONALTAX = (structure.PROFESSIONALTAX or 0) + (previous_salary.Deduction_YTD_PROFESSIONALTAX or 0)
        
        employee_salary.Deduction_Montly_GroupHealthInsurance = structure.GroupHealthInsurance
        employee_salary.Deduction_YTD_GroupHealthInsurance = (structure.GroupHealthInsurance or 0) + (previous_salary.Deduction_YTD_GroupHealthInsurance or 0)
        
        employee_salary.Deduction_Montly_OTHERS = 0
        employee_salary.Deduction_YTD_OTHERS = (previous_salary.Deduction_YTD_OTHERS or 0)
        
        employee_salary.Deduction_Montly_GROSSSDeduction = structure.GROSSDEDUCTIONS
        employee_salary.Deduction_YTD_GROSSSDeduction = (structure.GROSSDEDUCTIONS or 0) + (previous_salary.Deduction_YTD_GROSSSDeduction or 0)
        
        employee_salary.NETTRANSFER = (structure.GROSSEARNINGS or 0) - (structure.GROSSDEDUCTIONS or 0)
        employee_salary.NETPAY = (structure.GROSSEARNINGS or 0) - (structure.GROSSDEDUCTIONS or 0)
    
    @staticmethod
    def is_in_financial_year(
        salary_month: str, 
        salary_year: str, 
        target_month: str, 
        target_year: str
    ) -> bool:
        """Check if a salary belongs to the same financial year as target"""
        month_order = {
            'January': 1, 'February': 2, 'March': 3, 'April': 4,
            'May': 5, 'June': 6, 'July': 7, 'August': 8,
            'September': 9, 'October': 10, 'November': 11, 'December': 12
        }
        salary_month_num = month_order.get(salary_month, 0)
        target_month_num = month_order.get(target_month, 0)
        salary_year_int = int(salary_year)
        target_year_int = int(target_year)
        
        # For target months April to December
        if target_month_num >= 4:
            # Salary months April to December must be in same year
            if salary_month_num >= 4:
                return salary_year_int == target_year_int
            # Salary months January to March belong to next year's financial year
            else:
                return salary_year_int == target_year_int + 1
        # For target months January to March
        else:
            # Salary months April to December belong to previous year's financial year
            if salary_month_num >= 4:
                return salary_year_int == target_year_int - 1
            # Salary months January to March must be in same year
            else:
                return salary_year_int == target_year_int