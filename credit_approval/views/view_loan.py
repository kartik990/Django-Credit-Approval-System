from django.http import JsonResponse
from credit_approval.models import Loan, Customer

def view_loan(request, loan_id):
    try:
        # Get loan object by loan_id
        loan = Loan.objects.get(pk=loan_id)
        
        # Get customer details associated with the loan
        customer_details = {
            'id': loan.customer.customer_id,
            'first_name': loan.customer.first_name,
            'last_name': loan.customer.last_name,
            'phone_number': loan.customer.phone_number,
            'age': loan.customer.age
        }
        
        response_data = {
            'loan_id': loan.loan_id,
            'customer': customer_details,
            'loan_amount': loan.loan_amount,
            'interest_rate': loan.interest_rate,
            'monthly_installment': loan.monthly_repayment,
            'tenure': loan.tenure
        }
        return JsonResponse(response_data)
    except Loan.DoesNotExist:
        return JsonResponse({'error': 'Loan not found'}, status=404)
