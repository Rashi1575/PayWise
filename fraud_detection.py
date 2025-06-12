
from ..utils.db import get_connection
import pandas as pd

class FraudDetector:
    def __init__(self):
        self.conn = get_connection()

    def check_unusual_amount(self, user_id, amount):
        """Check if amount is significantly higher than user's average"""
        avg_query = """
            SELECT AVG(amount) FROM payments 
            WHERE user_id = %s AND date > CURRENT_DATE - INTERVAL '3 months'
        """
        avg_amount = pd.read_sql(avg_query, self.conn, params=(user_id,)).iloc[0,0] or 0
        return amount > (avg_amount * 5)  # 5x average is suspicious

    def validate_ip(self, user_id, ip_address):
        """Simple IP validation (expand with geolocation API)"""
        # In production, integrate with ipapi.co or similar
        return True

    def luhn_check(self, card_number):
        """Validate card number using Luhn algorithm"""
        def digits_of(n):
            return [int(d) for d in str(n)]
        digits = digits_of(card_number)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d*2))
        return checksum % 10 == 0

    def __del__(self):
        self.conn.close()