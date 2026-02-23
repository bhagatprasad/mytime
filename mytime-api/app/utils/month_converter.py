class MonthToYearConverter:
    @staticmethod
    def get_days_in_month(month: str, year: int) -> int:
        month_days = {
            'January': 31, 'February': 28, 'March': 31, 'April': 30,
            'May': 31, 'June': 30, 'July': 31, 'August': 31,
            'September': 30, 'October': 31, 'November': 30, 'December': 31
        }
        
        days = month_days.get(month, 30)
        
        if month == 'February' and MonthToYearConverter.is_leap_year(year):
            days = 29
            
        return days
    
    @staticmethod
    def get_adjusted_month_number(month: str, year: int) -> int:
        month_order = {
            'April': 1, 'May': 2, 'June': 3, 'July': 4,
            'August': 5, 'September': 6, 'October': 7, 'November': 8,
            'December': 9, 'January': 10, 'February': 11, 'March': 12
        }
        return month_order.get(month, 0)
    
    @staticmethod
    def is_leap_year(year: int) -> bool:
        return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)