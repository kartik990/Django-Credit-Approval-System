from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField( max_length=15)
    age = models.PositiveIntegerField(default=0)
    monthly_salary = models.DecimalField(max_digits=10, decimal_places=2)
    approved_limit = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Loan(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    loan_id = models.AutoField(primary_key=True)
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    tenure = models.IntegerField()
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    monthly_repayment = models.DecimalField(max_digits=10, decimal_places=2)
    emis_paid_on_time = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Loan ID: {self.loan_id} | Customer: {self.customer}"

@receiver(pre_save, sender=Customer)
def auto_increment_customer_id(sender, instance, **kwargs):
    if not instance.customer_id:
        max_id = Customer.objects.aggregate(models.Max('customer_id'))['customer_id__max']
        instance.customer_id = max_id + 1 if max_id else 1

@receiver(pre_save, sender=Loan)
def auto_increment_loan_id(sender, instance, **kwargs):
    if not instance.loan_id:
        max_id = Loan.objects.aggregate(models.Max('loan_id'))['loan_id__max']
        instance.loan_id = max_id + 1 if max_id else 1