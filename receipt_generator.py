from fpdf import FPDF  # Make sure fpdf2 is installed
import os
from datetime import datetime

class ReceiptGenerator:
    @staticmethod
    def generate(user_id, payment_data, rewards=None):
        pdf = FPDF()
        pdf.add_page()
        
        # Header
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, 'Payment Receipt', 0, 1, 'C')
        
        # Payment details
        pdf.set_font('Arial', '', 12)
        details = [
            f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Transaction ID: {payment_data['order_id']}",
            f"User ID: {user_id}",
            f"Amount: ₹{payment_data['amount']:.2f}",
            f"Category: {payment_data['category']}",
            f"Description: {payment_data['description']}"
        ]
        
        for line in details:
            pdf.cell(0, 10, line, 0, 1)
        
        # Rewards section if applicable
        if rewards:
            pdf.cell(0, 10, 'Applied Rewards:', 0, 1)
            for reward in rewards:
                pdf.cell(0, 10, f"- {reward}", 0, 1)
        
        # Save receipt
        os.makedirs(f'receipts/{user_id}', exist_ok=True)
        filename = f"receipts/{user_id}/{payment_data['order_id']}.pdf"
        pdf.output(filename)
        return filename