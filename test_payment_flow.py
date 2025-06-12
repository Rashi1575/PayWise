import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.payments.gateway import PaymentGateway

def run_tests():
    gateway = PaymentGateway()
    
    # Test 1: Normal successful payment
    print("\n=== Test 1: Successful Payment ===")
    result = gateway.process_payment(
        user_id="test_user_1",
        amount=1500,
        category="Shopping",
        description="Test purchase",
        payment_method="test_card_valid",
        ip_address="127.0.0.1"
    )
    print_result(result)

    # Test 2: Budget exceeded
    print("\n=== Test 2: Budget Warning ===")
    result = gateway.process_payment(
        user_id="test_user_1",
        amount=4500,
        category="Shopping",
        description="Large purchase",
        payment_method="test_card_valid",
        ip_address="127.0.0.1"
    )
    print_result(result)

    # Test 3: Savings category
    print("\n=== Test 3: Savings Payment ===")
    result = gateway.process_payment(
        user_id="test_user_1",
        amount=2000,
        category="Savings",
        description="Monthly savings",
        payment_method="test_card_valid",
        ip_address="127.0.0.1"
    )
    print_result(result)

def print_result(result):
    print("Status:", result['status'])
    if 'message' in result:
        print("Message:", result['message'])
    if 'receipt' in result:
        print("Receipt generated at:", result['receipt'])
    if 'rewards' in result:
        print("Applied rewards:", result['rewards'])
    print("---")

if __name__ == "__main__":
    run_tests()