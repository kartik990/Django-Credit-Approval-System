from django.http import JsonResponse
from credit_approval.models import Loan

def view_loans_by_customer(request, customer_id):
    try:
        # Get all loans associated with the customer_id
        loans = Loan.objects.filter(customer__customer_id=customer_id)
        
        loan_items = []
        for loan in loans:
            loan_item = {
                'loan_id': loan.loan_id,
                'loan_amount': loan.loan_amount,
                'interest_rate': loan.interest_rate,
                'monthly_installment': loan.monthly_repayment,
                'repayments_left': loan.tenure - loan.emis_paid_on_time  
            }
            loan_items.append(loan_item)
        
        return JsonResponse(loan_items, safe=False)
    
    except Loan.DoesNotExist:
        return JsonResponse({'error': 'No loans found for this customer'}, status=404)
