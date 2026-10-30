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
    MonthlySalaryMultiCreate,
    MonthlySalaryUpdate
)
from app.utils.month_converter import MonthToYearConverter
from app.utils.indian_salary_converter import IndianSalaryConverter
import math

logger = logging.getLogger(__name__)


# ============================================================================
# Month / Financial Year helpers (module-level, robust to all month formats)
# ============================================================================
MONTH_NAME_TO_NUM = {
    "JAN": 1, "JANUARY": 1,
    "FEB": 2, "FEBRUARY": 2,
    "MAR": 3, "MARCH": 3,
    "APR": 4, "APRIL": 4,
    "MAY": 5,
    "JUN": 6, "JUNE": 6,
    "JUL": 7, "JULY": 7,
    "AUG": 8, "AUGUST": 8,
    "SEP": 9, "SEPT": 9, "SEPTEMBER": 9,
    "OCT": 10, "OCTOBER": 10,
    "NOV": 11, "NOVEMBER": 11,
    "DEC": 12, "DECEMBER": 12,
}


def _month_to_num(month_value) -> int:
    """Accept 1..12, '04', 'April', 'APR', 4 → 1..12 (0 if invalid)."""
    if month_value is None:
        return 0
    if isinstance(month_value, int):
        return month_value if 1 <= month_value <= 12 else 0
    s = str(month_value).strip().upper()
    if s.isdigit():
        n = int(s)
        return n if 1 <= n <= 12 else 0
    return MONTH_NAME_TO_NUM.get(s, 0)


def _month_index_in_fy(month_value, year: int) -> int:
    """
    Position of month inside the financial year (April=1 ... March=12).
    This is the YTD multiplier: YTD = Monthly × month_index.
    """
    m = _month_to_num(month_value)
    if m == 0:
        return 0
    if m >= 4:
        return m - 3          # Apr=1 ... Dec=9
    return m + 9              # Jan=10, Feb=11, Mar=12


# ============================================================================
# MonthlySalaryService
# ============================================================================
class MonthlySalaryService:

    # ------------------------------------------------------------------ fetch
    @staticmethod
    def fetch_monthly_salary(db: Session, salary_id: int) -> Optional[MonthlySalary]:
        return db.query(MonthlySalary).filter(MonthlySalary.MonthlySalaryId == salary_id).first()

    @staticmethod
    def fetch_all_monthly_salaries(db: Session) -> List[MonthlySalary]:
        return db.query(MonthlySalary).all()

    @staticmethod
    def fetch_all_monthly_salaries_with_employees(db: Session) -> List[MonthlySalary]:
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
        record = (
            db.query(MonthlySalary)
            .options(selectinload(MonthlySalary.employee_salaries))
            .filter(MonthlySalary.MonthlySalaryId == salary_id)
            .first()
        )
        if record is None:
            return None
        if is_active_employees is not None:
            record.employee_salaries = [
                emp for emp in record.employee_salaries
                if emp.IsActive == is_active_employees
            ]
        return record

    # --------------------------------------------------------------- CRUD
    @staticmethod
    def create_monthly_salary(db: Session, salary_data: MonthlySalaryCreate) -> MonthlySalary:
        salary_dict = salary_data.model_dump(exclude_unset=True)
        salary = MonthlySalary(**salary_dict)
        db.add(salary)
        db.commit()
        db.refresh(salary)
        logger.info(f"Created monthly salary with ID: {salary.MonthlySalaryId}")
        return salary

    @staticmethod
    def update_monthly_salary(db: Session, salary_id: int, salary_data: MonthlySalaryUpdate) -> MonthlySalary:
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
        if isinstance(salary_data, dict):
            if salary_id:
                salary_data = MonthlySalaryUpdate(**salary_data)
            else:
                salary_data = MonthlySalaryCreate(**salary_data)
        if salary_id:
            return MonthlySalaryService.update_monthly_salary(db, salary_id, salary_data)
        return MonthlySalaryService.create_monthly_salary(db, salary_data)

    @staticmethod
    def delete_monthly_salary(db: Session, salary_id: int) -> bool:
        salary = db.query(MonthlySalary).filter(MonthlySalary.MonthlySalaryId == salary_id).first()
        if not salary:
            raise ValueError(f"Monthly salary record with ID {salary_id} not found for deletion")
        db.delete(salary)
        db.commit()
        logger.info(f"Deleted monthly salary with ID: {salary_id}")
        return True

    # --------------------------------------------------- Month / FY helpers
    @staticmethod
    def is_april_month(month: str) -> bool:
        """Check if given month is April — accepts 'April', 'APR', '4', '04'."""
        return _month_to_num(month) == 4

    @staticmethod
    def get_financial_year(month: str, year: int) -> Tuple[int, int]:
        """
        Indian FY: April (Y) → March (Y+1).
        April 2025 → (2025, 2026)
        March 2026 → (2025, 2026)
        """
        m = _month_to_num(month)
        if m >= 4:
            return (year, year + 1)
        return (year - 1, year)

    @staticmethod
    def is_in_financial_year(
        salary_month: str,
        salary_year: str,
        target_month: str,
        target_year: str
    ) -> bool:
        """Check if a salary belongs to the same financial year as target."""
        sal_num = _month_to_num(salary_month)
        tgt_num = _month_to_num(target_month)
        sal_year = int(salary_year)
        tgt_year = int(target_year)

        if tgt_num >= 4:
            # Target Apr..Dec → FY runs tgt_year -> tgt_year+1
            if sal_num >= 4:
                return sal_year == tgt_year
            return sal_year == tgt_year + 1
        else:
            # Target Jan..Mar → FY runs tgt_year-1 -> tgt_year
            if sal_num >= 4:
                return sal_year == tgt_year - 1
            return sal_year == tgt_year

    @staticmethod
    def get_previous_salaries_in_current_financial_year(
        db: Session,
        employee_id: int,
        current_month: str,
        current_year: str,
        current_monthly_salary_id: int
    ) -> List[EmployeeSalary]:
        """
        Return prior salaries in the SAME financial year, ordered oldest→newest.
        Kept for backwards compatibility; the new YTD logic uses month-index,
        so this is only informational / for auditing.
        """
        current_year_int = int(current_year)
        current_num = _month_to_num(current_month)
        fy_start, fy_end = MonthlySalaryService.get_financial_year(current_month, current_year_int)

        all_salaries = db.query(EmployeeSalary).filter(
            EmployeeSalary.EmployeeId == employee_id,
            EmployeeSalary.MonthlySalaryId != current_monthly_salary_id,
            EmployeeSalary.IsActive == True
        ).all()

        current_key = (current_year_int, current_num)
        prev: List[EmployeeSalary] = []

        for sal in all_salaries:
            s_num = _month_to_num(sal.SalaryMonth)
            s_year = int(sal.SalaryYear)

            # FY membership check
            s_fy_start = s_year if s_num >= 4 else s_year - 1
            if s_fy_start != fy_start:
                continue

            if (s_year, s_num) < current_key:
                prev.append(sal)

        prev.sort(key=lambda x: (int(x.SalaryYear), _month_to_num(x.SalaryMonth)))
        return prev

    # ================================================================
    # CORE YTD APPLIER — single source of truth
    # ================================================================
    @staticmethod
    def _apply_salary_with_ytd(
        employee_salary: EmployeeSalary,
        structure: EmployeeSalaryStructure,
        month_index: int
    ) -> None:
        """
        Apply monthly + YTD values using:
            YTD = Monthly × month_index_in_financial_year
        (April index=1 → reset; May index=2; … March index=12)

        This is applied to EVERY earnings & deductions field so nothing
        can drift out of sync.
        """
        def ytd(monthly):
            return int(round((monthly or 0) * month_index))

        # ---------- Earnings ----------
        employee_salary.Earning_Monthly_Basic           = structure.BASIC or 0
        employee_salary.Earning_YTD_Basic               = ytd(structure.BASIC)

        employee_salary.Earning_Monthly_HRA             = structure.HRA or 0
        employee_salary.Earning_YTD_HRA                 = ytd(structure.HRA)

        employee_salary.Earning_Monthly_CONVEYANCE      = structure.CONVEYANCE or 0
        employee_salary.Earning_YTD_CONVEYANCE          = ytd(structure.CONVEYANCE)

        employee_salary.Earning_Monthly_MEDICALALLOWANCE = structure.MEDICALALLOWANCE or 0
        employee_salary.Earning_YTD_MEDICALALLOWANCE    = ytd(structure.MEDICALALLOWANCE)

        employee_salary.Earning_Monthly_SPECIALALLOWANCE = structure.SPECIALALLOWANCE or 0
        employee_salary.Earning_YTD_SPECIALALLOWANCE    = ytd(structure.SPECIALALLOWANCE)

        employee_salary.Earning_Monthly_SPECIALBONUS    = getattr(structure, "SPECIALBONUS", 0) or 0
        employee_salary.Earning_YTD_SPECIALBONUS        = ytd(employee_salary.Earning_Monthly_SPECIALBONUS)

        employee_salary.Earning_Monthly_STATUTORYBONUS  = structure.STATUTORYBONUS or 0
        employee_salary.Earning_YTD_STATUTORYBONUS      = ytd(structure.STATUTORYBONUS)

        employee_salary.Earning_Monthly_OTHERS          = structure.OTHERS or 0
        employee_salary.Earning_YTD_OTHERS              = ytd(structure.OTHERS)

        employee_salary.Earning_Monthly_GROSSEARNINGS   = structure.GROSSEARNINGS or 0
        employee_salary.Earning_YTD_GROSSEARNINGS       = ytd(structure.GROSSEARNINGS)

        # ---------- Deductions ----------
        employee_salary.Deduction_Monthly_ProvidentFund = structure.PF or 0
        employee_salary.Deduction_YTD_ProvidentFund     = ytd(structure.PF)

        employee_salary.Deduction_Monthly_PROFESSIONALTAX = structure.PROFESSIONALTAX or 0
        employee_salary.Deduction_YTD_PROFESSIONALTAX     = ytd(structure.PROFESSIONALTAX)

        employee_salary.Deduction_Monthly_GroupHealthInsurance = structure.GroupHealthInsurance or 0
        employee_salary.Deduction_YTD_GroupHealthInsurance     = ytd(structure.GroupHealthInsurance)

        employee_salary.Deduction_Monthly_OTHERS        = 0
        employee_salary.Deduction_YTD_OTHERS            = 0

        employee_salary.Deduction_Monthly_GROSSSDeduction = structure.GROSSDEDUCTIONS or 0
        employee_salary.Deduction_YTD_GROSSSDeduction     = ytd(structure.GROSSDEDUCTIONS)

        # ---------- Net ----------
        employee_salary.NETPAY = (structure.GROSSEARNINGS or 0) - (structure.GROSSDEDUCTIONS or 0)
        employee_salary.NETTRANSFER = employee_salary.NETPAY

    # ================================================================
    # PUBLISH: single monthly salary
    # ================================================================
    @staticmethod
    def publish_monthly_salary(db: Session, monthly_salary: MonthlySalary) -> Tuple[bool, int]:
        logger.info(
            f"Starting publish for monthly salary ID: {monthly_salary.MonthlySalaryId}, "
            f"Month: {monthly_salary.SalaryMonth} {monthly_salary.SalaryYear}"
        )

        salary_year_int = int(monthly_salary.SalaryYear)
        salary_month_num = _month_to_num(monthly_salary.SalaryMonth)
        if salary_month_num == 0:
            logger.error(f"Invalid SalaryMonth: {monthly_salary.SalaryMonth}")
            return False, 0

        month_index = _month_index_in_fy(salary_month_num, salary_year_int)
        fy_start, fy_end = MonthlySalaryService.get_financial_year(
            monthly_salary.SalaryMonth, salary_year_int
        )
        logger.info(
            f"FY={fy_start}-{fy_end}, month_index={month_index} "
            f"(April=1 reset, March=12)"
        )

        # Existing employee salaries (for update path)
        existing_employee_salaries = db.query(EmployeeSalary).filter(
            EmployeeSalary.MonthlySalaryId == monthly_salary.MonthlySalaryId
        ).all()
        existing_by_emp: Dict[int, EmployeeSalary] = {
            es.EmployeeId: es for es in existing_employee_salaries
        }
        is_update = len(existing_employee_salaries) > 0
        if is_update:
            logger.info(
                f"Monthly salary {monthly_salary.MonthlySalaryId} is being updated "
                f"with {len(existing_employee_salaries)} existing employee records"
            )

        # Active employees
        active_employee_ids = [
            emp.EmployeeId for emp in db.query(Employee.EmployeeId)
                                        .filter(Employee.IsActive == True).all()
        ]
        if not active_employee_ids:
            logger.warning(f"No active employees found for monthly salary {monthly_salary.MonthlySalaryId}")
            return False, 0

        # Salary structures
        salary_structures = db.query(EmployeeSalaryStructure).filter(
            EmployeeSalaryStructure.EmployeeId.in_(active_employee_ids),
            EmployeeSalaryStructure.IsActive == True
        ).all()
        if not salary_structures:
            logger.warning("No salary structures found for active employees")
            return False, 0

        standard_days = MonthToYearConverter.get_days_in_month(
            monthly_salary.SalaryMonth, salary_year_int
        )
        lop_days = 0

        employee_salaries_to_add: List[EmployeeSalary] = []
        employee_salaries_to_update: List[EmployeeSalary] = []

        for structure in salary_structures:
            emp_id = structure.EmployeeId
            existing = existing_by_emp.get(emp_id)

            if existing:
                emp_salary = existing
                MonthlySalaryService._update_employee_salary_from_monthly(
                    emp_salary, monthly_salary, standard_days, lop_days
                )
                employee_salaries_to_update.append(emp_salary)
                logger.info(f"Updating existing salary for employee {emp_id}")
            else:
                emp_salary = EmployeeSalary()
                emp_salary.MonthlySalaryId = monthly_salary.MonthlySalaryId
                emp_salary.EmployeeId      = emp_id
                emp_salary.Title           = monthly_salary.Title
                emp_salary.SalaryMonth     = monthly_salary.SalaryMonth
                emp_salary.SalaryYear      = monthly_salary.SalaryYear
                emp_salary.LOCATION        = monthly_salary.Location
                emp_salary.STDDAYS         = standard_days
                emp_salary.LOPDAYS         = lop_days
                emp_salary.WRKDAYS         = standard_days
                emp_salary.CreatedBy       = monthly_salary.CreatedBy
                emp_salary.ModifiedBy      = monthly_salary.ModifiedBy
                emp_salary.CreatedOn       = monthly_salary.CreatedOn
                emp_salary.ModifiedOn      = monthly_salary.ModifiedOn
                emp_salary.IsActive        = True
                employee_salaries_to_add.append(emp_salary)
                logger.info(f"Creating new salary for employee {emp_id}")

            # ---- THE FIX: month-index based YTD (applies to every field) ----
            MonthlySalaryService._apply_salary_with_ytd(
                emp_salary, structure, month_index
            )

            net_salary = (structure.GROSSEARNINGS or 0) - (structure.GROSSDEDUCTIONS or 0)
            emp_salary.INWords = IndianSalaryConverter.convert_to_words(net_salary)

            logger.info(
                f"Employee {emp_id} — MonthIdx={month_index} | "
                f"MonthlyBasic={emp_salary.Earning_Monthly_Basic} "
                f"YTD_Basic={emp_salary.Earning_YTD_Basic} | "
                f"MonthlyHRA={emp_salary.Earning_Monthly_HRA} "
                f"YTD_HRA={emp_salary.Earning_YTD_HRA} | "
                f"MonthlyGross={emp_salary.Earning_Monthly_GROSSEARNINGS} "
                f"YTD_Gross={emp_salary.Earning_YTD_GROSSEARNINGS} | "
                f"MonthlyPF={emp_salary.Deduction_Monthly_ProvidentFund} "
                f"YTD_PF={emp_salary.Deduction_YTD_ProvidentFund} | "
                f"Net={emp_salary.NETPAY}"
            )

        if employee_salaries_to_add:
            db.add_all(employee_salaries_to_add)
            logger.info(f"Added {len(employee_salaries_to_add)} new employee salaries")

        if employee_salaries_to_update:
            logger.info(f"Updated {len(employee_salaries_to_update)} existing employee salaries")

        db.commit()

        total_processed = len(employee_salaries_to_add) + len(employee_salaries_to_update)
        logger.info(
            f"Successfully published monthly salary {monthly_salary.MonthlySalaryId} "
            f"for {total_processed} employees"
        )
        return True, total_processed

    # ================================================================
    # PUBLISH: multi-month multi-employee
    # ================================================================
    @staticmethod
    def publish_monthly_multiple_salary(
        db: Session,
        payload: MonthlySalaryMultiCreate
    ) -> Tuple[bool, int]:
        employee_ids: List[int] = [
            int(eid.strip()) for eid in payload.EmployeeIds.split(",") if eid.strip()
        ]
        salary_months: List[str] = [
            m.strip() for m in payload.SalaryMonths.split(",") if m.strip()
        ]

        if not employee_ids:
            logger.warning("No employee IDs provided.")
            return False, 0
        if not salary_months:
            logger.warning("No salary months provided.")
            return False, 0

        salary_year = payload.SalaryYear

        active_employees = db.query(Employee).filter(
            Employee.EmployeeId.in_(employee_ids),
            Employee.IsActive == True
        ).all()
        active_employee_ids = [emp.EmployeeId for emp in active_employees]
        if not active_employee_ids:
            logger.warning("None of the provided employee IDs are active.")
            return False, 0

        salary_structures = db.query(EmployeeSalaryStructure).filter(
            EmployeeSalaryStructure.EmployeeId.in_(active_employee_ids),
            EmployeeSalaryStructure.IsActive == True
        ).all()
        structure_map: Dict[int, EmployeeSalaryStructure] = {
            s.EmployeeId: s for s in salary_structures
        }
        if not structure_map:
            logger.warning("No active salary structures found for provided employees.")
            return False, 0

        now = datetime.utcnow()
        total_processed = 0

        for salary_month in salary_months:
            title = f"Pay Slip for the month of {salary_month} {salary_year}"
            standard_days = MonthToYearConverter.get_days_in_month(
                salary_month, int(salary_year)
            )
            lop_days = 0

            monthly_salary = db.query(MonthlySalary).filter(
                MonthlySalary.SalaryMonth == salary_month,
                MonthlySalary.SalaryYear == salary_year,
                MonthlySalary.Location == payload.Location,
            ).first()

            if monthly_salary is None:
                monthly_salary = MonthlySalary()
                monthly_salary.Title       = title
                monthly_salary.SalaryMonth = salary_month
                monthly_salary.SalaryYear  = salary_year
                monthly_salary.Location    = payload.Location
                monthly_salary.StdDays     = standard_days
                monthly_salary.WrkDays     = standard_days
                monthly_salary.LopDays     = lop_days
                monthly_salary.IsActive    = True
                monthly_salary.CreatedBy   = payload.CreatedBy
                monthly_salary.ModifiedBy  = payload.CreatedBy
                monthly_salary.CreatedOn   = now
                monthly_salary.ModifiedOn  = now
                db.add(monthly_salary)
                db.flush()
                logger.info(f"Created MonthlySalary header: '{title}' (ID={monthly_salary.MonthlySalaryId})")
            else:
                logger.info(f"Using existing MonthlySalary header: '{title}' (ID={monthly_salary.MonthlySalaryId})")

            # Month index in FY — the YTD multiplier
            month_index = _month_index_in_fy(salary_month, int(salary_year))
            logger.info(
                f"[{salary_month} {salary_year}] month_index={month_index} "
                f"(April=1 reset, March=12)"
            )

            existing_employee_salaries = db.query(EmployeeSalary).filter(
                EmployeeSalary.MonthlySalaryId == monthly_salary.MonthlySalaryId,
                EmployeeSalary.EmployeeId.in_(active_employee_ids)
            ).all()
            existing_map: Dict[int, EmployeeSalary] = {
                es.EmployeeId: es for es in existing_employee_salaries
            }

            employee_salaries_to_add: List[EmployeeSalary] = []
            employee_salaries_to_update: List[EmployeeSalary] = []

            for emp_id in active_employee_ids:
                structure = structure_map.get(emp_id)
                if not structure:
                    logger.warning(f"No salary structure for employee {emp_id}, skipping.")
                    continue

                existing_es = existing_map.get(emp_id)

                if existing_es:
                    emp_salary = existing_es
                    MonthlySalaryService._update_employee_salary_from_monthly(
                        emp_salary, monthly_salary, standard_days, lop_days
                    )
                    employee_salaries_to_update.append(emp_salary)
                    logger.info(f"[{salary_month} {salary_year}] Updating existing salary for employee {emp_id}")
                else:
                    emp_salary = EmployeeSalary()
                    emp_salary.MonthlySalaryId = monthly_salary.MonthlySalaryId
                    emp_salary.EmployeeId      = emp_id
                    emp_salary.Title           = title
                    emp_salary.SalaryMonth     = salary_month
                    emp_salary.SalaryYear      = salary_year
                    emp_salary.LOCATION        = payload.Location
                    emp_salary.STDDAYS         = standard_days
                    emp_salary.LOPDAYS         = lop_days
                    emp_salary.WRKDAYS         = standard_days
                    emp_salary.CreatedBy       = payload.CreatedBy
                    emp_salary.ModifiedBy      = payload.CreatedBy
                    emp_salary.CreatedOn       = now
                    emp_salary.ModifiedOn      = now
                    emp_salary.IsActive        = True
                    employee_salaries_to_add.append(emp_salary)
                    logger.info(f"[{salary_month} {salary_year}] Creating new salary for employee {emp_id}")

                # ---- THE FIX: month-index based YTD (all fields) ----
                MonthlySalaryService._apply_salary_with_ytd(
                    emp_salary, structure, month_index
                )

                net_salary = (structure.GROSSEARNINGS or 0) - (structure.GROSSDEDUCTIONS or 0)
                emp_salary.INWords = IndianSalaryConverter.convert_to_words(net_salary)

                logger.info(
                    f"[{salary_month} {salary_year}] Emp {emp_id} — "
                    f"MonthIdx={month_index} | "
                    f"Basic={emp_salary.Earning_Monthly_Basic}/YTD={emp_salary.Earning_YTD_Basic} | "
                    f"HRA={emp_salary.Earning_Monthly_HRA}/YTD={emp_salary.Earning_YTD_HRA} | "
                    f"Gross={emp_salary.Earning_Monthly_GROSSEARNINGS}/YTD={emp_salary.Earning_YTD_GROSSEARNINGS}"
                )

            if employee_salaries_to_add:
                db.add_all(employee_salaries_to_add)
                logger.info(f"[{salary_month} {salary_year}] Added {len(employee_salaries_to_add)} new employee salary records")
            if employee_salaries_to_update:
                logger.info(f"[{salary_month} {salary_year}] Updated {len(employee_salaries_to_update)} employee salary records")

            total_processed += len(employee_salaries_to_add) + len(employee_salaries_to_update)

        db.commit()
        logger.info(
            f"Successfully published salaries for {len(salary_months)} month(s), "
            f"{total_processed} total records."
        )
        return True, total_processed

    # ================================================================
    # Helpers
    # ================================================================
    @staticmethod
    def _update_employee_salary_from_monthly(
        employee_salary: EmployeeSalary,
        monthly_salary: MonthlySalary,
        standard_days: int,
        lop_days: int
    ) -> None:
        """Update header-ish fields that live on the MonthlySalary record."""
        employee_salary.Title       = monthly_salary.Title
        employee_salary.SalaryMonth = monthly_salary.SalaryMonth
        employee_salary.SalaryYear  = monthly_salary.SalaryYear
        employee_salary.LOCATION    = monthly_salary.Location
        employee_salary.STDDAYS     = standard_days
        employee_salary.LOPDAYS     = lop_days
        employee_salary.WRKDAYS     = standard_days
        employee_salary.ModifiedOn  = monthly_salary.ModifiedOn
        employee_salary.ModifiedBy  = monthly_salary.ModifiedBy

    @staticmethod
    def check_if_reprocessing_needed(
        old_salary: MonthlySalary,
        new_data: MonthlySalaryUpdate
    ) -> bool:
        update_data = new_data.model_dump(exclude_unset=True)
        employee_impacting_fields = {
            'Title', 'SalaryMonth', 'SalaryYear', 'Location',
            'StdDays', 'WrkDays', 'LopDays'
        }
        changed = set(update_data.keys())
        needs = bool(changed & employee_impacting_fields)
        if needs:
            logger.info(f"Reprocessing needed due to changes in: {changed & employee_impacting_fields}")
        return needs

    # ---- Legacy helpers kept for API compatibility, delegating to new logic ----
    @staticmethod
    def _set_first_month_of_financial_year(
        employee_salary: EmployeeSalary,
        structure: EmployeeSalaryStructure
    ) -> None:
        """
        DEPRECATED — kept for backward compatibility.
        Equivalent to month_index = 1 (April / first month in FY).
        """
        MonthlySalaryService._apply_salary_with_ytd(employee_salary, structure, month_index=1)

    @staticmethod
    def _set_subsequent_salaries(
        employee_salary: EmployeeSalary,
        structure: EmployeeSalaryStructure,
        previous_salary: EmployeeSalary
    ) -> None:
        """
        DEPRECATED — kept for backward compatibility.

        Determines month_index from previous_salary + 1 month and delegates to
        the month-index based applier. This preserves the *correct* result
        even if a caller still uses the old API.
        """
        prev_num = _month_to_num(previous_salary.SalaryMonth)
        prev_year = int(previous_salary.SalaryYear)

        # Advance one calendar month
        if prev_num == 12:
            next_num, next_year = 1, prev_year + 1
        else:
            next_num, next_year = prev_num + 1, prev_year

        month_index = _month_index_in_fy(next_num, next_year)
        MonthlySalaryService._apply_salary_with_ytd(
            employee_salary, structure, month_index
        )