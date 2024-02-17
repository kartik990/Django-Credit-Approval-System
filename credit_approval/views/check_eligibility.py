from django.http import JsonResponse
from django.db import connection
import json
from credit_approval.utils import calculate_credit_score, calculate_monthly_installment


def check_eligibility(request):

    data = json.loads(request.body)

    customer_id = int(data.get('customer_id'))
    loan_amount = float(data.get('loan_amount'))
    interest_rate = float(data.get('interest_rate'))
    tenure = int(data.get('tenure'))
    
    # Calculating credit score 
    credit_score = calculate_credit_score(customer_id)
    
    # Check loan eligibility based on credit score and other conditions given in assignment
    if credit_score > 50:
        approval = True
        corrected_interest_rate = interest_rate
    elif 50 >= credit_score > 30:
        approval = True
        if interest_rate <= 12:
            corrected_interest_rate = 12
        else:
            corrected_interest_rate = interest_rate
    elif 30 >= credit_score > 10:
        approval = True
        if interest_rate <= 16:
            corrected_interest_rate = 16
        else:
            corrected_interest_rate = interest_rate
    else:
        approval = False
        corrected_interest_rate = None
    
    
    response_data = {
        'customer_id': customer_id,
        'approval': approval,
        'interest_rate': interest_rate,
        'corrected_interest_rate': corrected_interest_rate,
        'tenure': tenure,
        'monthly_installment': calculate_monthly_installment(loan_amount, interest_rate, tenure)
    }
    
    return JsonResponse(response_data)

