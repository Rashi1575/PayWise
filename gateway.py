import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import razorpay
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv

from src.ml_models.fraud_detection import FraudDetector
from .receipt_generator import ReceiptGenerator
from src.dashboard.rewards import get_active_rewards, add_reward
from src.dashboard.target_tracker import update_monthly_savings
from src.utils.db import get_connection, get_user_email  # Updated import
from src.utils.email_service import send_email

load_dotenv()

class PaymentGateway:
    def __init__(self):
        self.client = razorpay.Client(
            auth=(os.getenv("RAZORPAY_KEY_ID"), os.getenv("RAZORPAY_KEY_SECRET"))
        )
        self.fraud_detector = FraudDetector()
        self.conn = get_connection()

    def process_payment(self, user_id, amount, category, description, payment_method, ip_address=None):
        try:
            # 1. Fraud checks
            if not self._run_fraud_checks(user_id, amount, payment_method, ip_address):
                return {"status": "failed", "reason": "Payment flagged as suspicious"}

            # 2. Budget check
            budget_status = self._check_budget(user_id, amount, category)
            if not budget_status["within_budget"]:
                return {"status": "warning", "message": budget_status["message"]}

            # 3. Create Razorpay order
            order = self._create_razorpay_order(user_id, amount, category, description)

            # 4. Record payment
            self._record_payment(
                user_id=user_id,
                amount=amount,
                category=category,
                description=description,
                payment_method=payment_method,
                order_id=order["id"]
            )

            # 5. Handle rewards
            applied_rewards = self._handle_rewards(user_id, category, amount)

            # 6. Update target tracker if savings
            if category == "Savings":
                update_monthly_savings(user_id, amount)

            # 7. Generate receipt
            receipt_path = ReceiptGenerator().generate(
                user_id=user_id,
                payment_data={
                    "order_id": order["id"],
                    "amount": amount,
                    "category": category,
                    "description": description
                },
                rewards=applied_rewards
            )

            # 8. Send notifications
            send_email(
                recipient=get_user_email(user_id),
                subject="Payment Confirmation",
                body=f"Your payment of ₹{amount:.2f} for {category} was successful.",
                attachment_path=receipt_path
            )

            return {
                "status": "success",
                "order_id": order["id"],
                "receipt": receipt_path,
                "rewards": applied_rewards
            }

        except Exception as e:
            return {"status": "error", "message": str(e)}

    def _run_fraud_checks(self, user_id, amount, payment_method, ip_address):
        if self.fraud_detector.check_unusual_amount(user_id, amount):
            return False
        if ip_address and not self.fraud_detector.validate_ip(user_id, ip_address):
            return False
        if payment_method.startswith("card") and not self.fraud_detector.luhn_check(payment_method[-16:]):
            return False
        return True

    def _check_budget(self, user_id, amount, category):
        query = """
            SELECT budget_amount, spent_amount FROM budgets 
            WHERE user_id = %s AND category = %s
        """
        result = pd.read_sql(query, self.conn, params=(user_id, category))
        
        if result.empty:
            return {"within_budget": True, "message": "No budget set"}
        
        budget, spent = result.iloc[0]
        new_total = spent + amount
        
        if new_total > budget:
            return {"within_budget": False, "message": f"Exceeds budget by ₹{new_total - budget:.2f}"}
        elif new_total > budget * 0.9:
            return {"within_budget": True, "message": "Approaching budget limit"}
        return {"within_budget": True, "message": "Within budget"}

    def _create_razorpay_order(self, user_id, amount, category, description):
        return self.client.order.create({
            "amount": int(amount * 100),
            "currency": "INR",
            "receipt": f"receipt_{user_id}_{datetime.now().timestamp()}",
            "notes": {
                "user_id": user_id,
                "category": category,
                "description": description
            }
        })

    def _record_payment(self, user_id, amount, category, description, payment_method, order_id):
        query = """
            INSERT INTO payments (
                user_id, amount, category, description, 
                payment_method, razorpay_order_id, date
            ) VALUES (%s, %s, %s, %s, %s, %s, NOW())
        """
        with self.conn.cursor() as cursor:
            cursor.execute(query, (
                user_id, amount, category, 
                description, payment_method, order_id
            ))
            self.conn.commit()

    def _handle_rewards(self, user_id, category, amount):
        rewards = get_active_rewards(user_id)
        applied = []
        
        for reward in rewards:
            if reward.category == category:
                applied.append(reward.name)
                self._mark_reward_used(user_id, reward.name)
        
        if amount > 1000 and category != "Savings":
            expiry = datetime.now() + timedelta(days=30)
            add_reward(
                user_id=user_id,
                reward_name=f"10% Cashback on next {category}",
                category=category,
                expiry_date=expiry
            )
        
        return applied

    def _mark_reward_used(self, user_id, reward_name):
        query = "UPDATE rewards SET used = TRUE WHERE user_id = %s AND reward_name = %s"
        with self.conn.cursor() as cursor:
            cursor.execute(query, (user_id, reward_name))
            self.conn.commit()

    def __del__(self):
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()
