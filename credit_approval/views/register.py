from django.http import JsonResponse
from django.core.exceptions import ValidationError
from credit_approval.models import Customer
import json
import math

def register_customer(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Extract data from JSON payload
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            age = data.get('age')
            monthly_salary = data.get('monthly_salary')
            phone_number = data.get('phone_number')

            if monthly_salary is not None:
                monthly_salary = float(monthly_salary)
                approved_limit = math.ceil(36 * monthly_salary / 100000) * 100000
            else:
                raise ValidationError("Monthly salary is required")

            # Create a new customer record
            customer = Customer.objects.create(
                first_name=first_name,
                last_name=last_name,
                age=age,
                monthly_salary=monthly_salary,
                phone_number=phone_number,
                approved_limit=approved_limit
            )

            response_data = {
                'name': f'{customer.first_name} {customer.last_name}',
                'age': customer.age,
                'monthly_income': customer.monthly_salary,
                'approved_limit': customer.approved_limit,
                'phone_number': customer.phone_number
            }

            return JsonResponse(response_data, status=201)
        
        except (ValueError, ValidationError) as e:
            error_message = str(e)
            return JsonResponse({'error': error_message}, status=400)
        
        except Exception as e:
            return JsonResponse({'error': 'An unexpected error occurred'}, status=500)

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
