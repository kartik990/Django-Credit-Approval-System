from django.http import JsonResponse
from credit_approval.models import Customer, Loan
from credit_approval.utils import calculate_credit_score, calculate_monthly_installment
from datetime import date, timedelta
import json


def create_loan(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        # Extracting data from request body
        customer_id = data.get('customer_id')
        if customer_id is None:
            raise ValueError("Customer ID must not be None")
        customer_id = int(customer_id)
        
        loan_amount = data.get('loan_amount')
        if loan_amount is None:
            raise ValueError("Loan amount must not be None")
        loan_amount = float(loan_amount)
        
        interest_rate = data.get('interest_rate')
        if interest_rate is None:
            raise ValueError("Interest rate must not be None")
        interest_rate = float(interest_rate)
        
        tenure = data.get('tenure')
        if tenure is None:
            raise ValueError("Tenure must not be None")
        tenure = int(tenure)

        
        # Check if customer exists
        try:
            customer = Customer.objects.get(customer_id=customer_id)
        except Customer.DoesNotExist:
            return JsonResponse({'error': 'Customer not found'}, status=400)
        
        credit_score = calculate_credit_score(customer_id)
        
        if credit_score > 50:
            approval = True
            corrected_interest_rate = interest_rate
            loan_approved_message = "Loan approved."
        elif 50 >= credit_score > 30:
            approval = True
            if interest_rate <= 12:
                corrected_interest_rate = 12
            else:
                corrected_interest_rate = interest_rate
            loan_approved_message = "Loan approved with corrected interest rate."
        elif 30 >= credit_score > 10:
            approval = True
            if interest_rate <= 16:
                corrected_interest_rate = 16
            else:
                corrected_interest_rate = interest_rate
            loan_approved_message = "Loan approved with corrected interest rate."
        else:
            approval = False
            corrected_interest_rate = None
            loan_approved_message = "Loan not approved due to low credit score."
        
        # Create Loan object if approved
        if approval:
            loan = Loan.objects.create(
                customer=customer,
                loan_amount=loan_amount,
                tenure=tenure,
                interest_rate=corrected_interest_rate,
                monthly_repayment=calculate_monthly_installment(loan_amount, corrected_interest_rate, tenure),
                emis_paid_on_time=0,  
                start_date=date.today(),  
                end_date = date.today() + timedelta(days=tenure * 30)
            )
            loan_id = loan.loan_id
            monthly_installment = loan.monthly_repayment
        else:
            loan_id = None
            monthly_installment = None
        
        # Construct response
        response_data = {
            'loan_id': loan_id,
            'customer_id': customer_id,
            'loan_approved': approval,
            'message': loan_approved_message,
            'monthly_installment': monthly_installment
        }
        
        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
