
import warnings
warnings.filterwarnings("ignore", category=UserWarning, message="pkg_resources is deprecated")
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
from dotenv import load_dotenv
from src.payments.gateway import PaymentGateway
load_dotenv()
# Test configuration
TEST_USER_ID = "test_user_123"
TEST_EMAIL = "test@example.com"  # Make sure this exists in your users 

def test_successful_payment():
    gateway = PaymentGateway()
    result = gateway.process_payment(
        user_id=TEST_USER_ID,
        amount=1000,
        category="Shopping",
        description="Test purchase",
        payment_method="test_card_valid",
        ip_address="127.0.0.1"
    )
    
    assert result['status'] == 'success'
    assert os.path.exists(result['receipt'])
    print(f"✅ Payment successful! Receipt: {result['receipt']}")
    print(f"Applied rewards: {result.get('rewards', [])}")
    
    
def test_budget_exceeded():
    gateway = PaymentGateway()
    result = gateway.process_payment(
        user_id=TEST_USER_ID,
        amount=2000,
        category="Shopping",
        description="Large test purchase",
        payment_method="test_card_valid",
        ip_address="127.0.0.1"
    )
    
    assert result['status'] == 'warning'
    assert "exceeds budget" in result['message']
    print(f"✅ Budget check working: {result['message']}")
    
def test_fraud_detection():
    gateway = PaymentGateway()
    result = gateway.process_payment(
        user_id=TEST_USER_ID,
        amount=10000,  # Unusually large amount
        category="Shopping",
        description="Suspicious purchase",
        payment_method="test_card_valid",
        ip_address="1.1.1.1"  # Suspicious IP
    )
    
    assert result['status'] == 'failed'
    assert "flagged as suspicious" in result['reason']
    print("✅ Fraud detection working")
    
def test_savings_payment():
    gateway = PaymentGateway()
    result = gateway.process_payment(
        user_id=TEST_USER_ID,
        amount=500,
        category="Savings",
        description="Monthly savings",
        payment_method="test_card_valid",
        ip_address="127.0.0.1"
    )
    
    assert result['status'] == 'success'
    print("✅ Savings payment processed")