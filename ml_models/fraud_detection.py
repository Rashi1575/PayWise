import sys
import os
import pandas as pd
import datetime
import re
import joblib  # For ML model
import requests
from dotenv import load_dotenv
load_dotenv()

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.utils.db import get_connection


class FraudDetector:
    def __init__(self):
        self.conn = get_connection()
        # Load a pretrained model (placeholder)
        try:
            self.model = joblib.load("fraud_model.pkl")  # Replace with your actual path
        except:
            self.model = None

    def check_unusual_amount(self, user_id, amount):
        """Check if amount is significantly higher than user's average"""
        avg_query = """
            SELECT AVG(amount) FROM payments 
            WHERE user_id = %s AND date > CURRENT_DATE - INTERVAL '3 months'
        """
        avg_amount = pd.read_sql(avg_query, self.conn, params=(user_id,)).iloc[0,0] or 0
        return amount > (avg_amount * 5)

    def luhn_check(self, card_number):
        def digits_of(n):
            return [int(d) for d in str(n)]
        digits = digits_of(card_number)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d * 2))
        return checksum % 10 == 0

    def expiry_check(self, expiry_date_str):
        try:
            now = datetime.datetime.now()
            month, year = map(int, expiry_date_str.split('/'))
            year += 2000 if year < 100 else 0
            exp_date = datetime.datetime(year, month, 1)
            return exp_date > now
        except Exception as e:
            print("Invalid expiry format:", e)
            return False

    def cvv_check(self, cvv):
        return re.fullmatch(r'\d{3,4}', str(cvv)) is not None

    def is_card_valid(self, card_number, expiry_date, cvv):
        return self.luhn_check(card_number) and self.expiry_check(expiry_date) and self.cvv_check(cvv)

    def check_velocity(self, user_id):
        velocity_query = """
            SELECT COUNT(*) FROM payments 
            WHERE user_id = %s AND timestamp > NOW() - INTERVAL '1 minute'
        """
        count = pd.read_sql(velocity_query, self.conn, params=(user_id,)).iloc[0, 0]
        return count > 5

    def check_geolocation_inconsistency(self, user_id, current_ip):
        """Compare current IP geolocation to previous IPs (mock logic)"""
        try:
            res = requests.get(f"https://ipapi.co/{current_ip}/json/").json()
            current_country = res.get("country")
        except:
            return False

        past_ips_query = """
            SELECT DISTINCT ip_address FROM payments 
            WHERE user_id = %s ORDER BY timestamp DESC LIMIT 5
        """
        ips = pd.read_sql(past_ips_query, self.conn, params=(user_id,))['ip_address'].tolist()
        for ip in ips:
            try:
                loc = requests.get(f"https://ipapi.co/{ip}/json/").json()
                if loc.get("country") != current_country:
                    return True
            except:
                continue
        return False

    def check_ip_risk_score(self, ip):
        try:
            API_KEY = os.getenv("QEKnilztVDoadIbIomG210X3Kftr8emm")
            url = f"https://ipqualityscore.com/api/json/ip/{API_KEY}/{ip}"
            res = requests.get(url, timeout=5).json()
            fraud_score = res.get("fraud_score", 0)
            is_proxy = res.get("proxy", False)
            is_tor = res.get("tor", False)
            return fraud_score > 50 or is_proxy or is_tor
        except Exception as e:
            print("IPQS API request failed:", e)
            return False

    def check_ml_anomaly(self, transaction_dict):
        try:
            df = pd.DataFrame([transaction_dict])
            return self.model.predict(df)[0] == 1
        except Exception as e:
            print("ML prediction failed:", e)
            return False

    def __del__(self):
        self.conn.close()
