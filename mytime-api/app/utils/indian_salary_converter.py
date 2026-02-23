class IndianSalaryConverter:
    """Utility class to convert numbers to Indian currency words"""
    
    ones = ['', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine',
            'Ten', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen',
            'Seventeen', 'Eighteen', 'Nineteen']
    tens = ['', '', 'Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy', 'Eighty', 'Ninety']

    @staticmethod
    def _below_hundred(n):
        if n < 20:
            return IndianSalaryConverter.ones[n]
        else:
            return (IndianSalaryConverter.tens[n // 10] + 
                    (' ' + IndianSalaryConverter.ones[n % 10] if n % 10 != 0 else ''))

    @staticmethod
    def _below_thousand(n):
        if n < 100:
            return IndianSalaryConverter._below_hundred(n)
        else:
            rest = IndianSalaryConverter._below_hundred(n % 100)
            return (IndianSalaryConverter.ones[n // 100] + ' Hundred' + 
                    (' ' + rest if rest else ''))

    @staticmethod
    def convert_to_words(amount: float) -> str:
        if not amount:
            return "Zero Rupees Only"
        
        rupees = int(amount)
        paise = round((amount - rupees) * 100)
        
        def rupees_to_words(n):
            if n == 0:
                return 'Zero'
            
            parts = []
            
            crore = n // 10000000
            n %= 10000000
            lakh = n // 100000
            n %= 100000
            thousand = n // 1000
            n %= 1000
            
            if crore:
                parts.append(IndianSalaryConverter._below_thousand(crore) + ' Crore')
            if lakh:
                parts.append(IndianSalaryConverter._below_thousand(lakh) + ' Lakh')
            if thousand:
                parts.append(IndianSalaryConverter._below_thousand(thousand) + ' Thousand')
            if n:
                parts.append(IndianSalaryConverter._below_thousand(n))
            
            return ' '.join(parts)
        
        result = rupees_to_words(rupees) + ' Rupees'
        if paise:
            result += ' and ' + rupees_to_words(paise) + ' Paise'
        result += ' Only'
        return result
