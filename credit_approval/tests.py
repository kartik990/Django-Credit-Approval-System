from django.test import TestCase, Client
from django.urls import reverse
from credit_approval.models import Customer

class RegisterCustomerViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register_customer_success(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'age': 30,
            'monthly_salary': 5000,
            'phone_number': '1234567890'
        }
        response = self.client.post(reverse('register_customer'), data=data, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Customer.objects.count(), 1)  # Ensure a customer record is created

        # Ensure the response contains the expected data
        self.assertEqual(response.json()['name'], 'John Doe')
        self.assertEqual(response.json()['age'], 30)
        self.assertEqual(response.json()['monthly_income'], 5000)
        # Add more assertions as needed



