from django.urls import path
from .views.register import register_customer
from .views.check_eligibility import check_eligibility
from .views.create_loan import create_loan
from .views.view_loan import view_loan
from .views.view_loans_by_customer import view_loans_by_customer 

urlpatterns = [
    path('register', register_customer, name='register_customer'),
    path('check-eligibility', check_eligibility, name='check_eligibility'),
    path('create-loan', create_loan, name='create_loan'),    
    path('view-loan/<loan_id>', view_loan, name='view_loan'),    
    path('view-loans/<customer_id>', view_loans_by_customer,name='view_loans_by_customer'),    
]
