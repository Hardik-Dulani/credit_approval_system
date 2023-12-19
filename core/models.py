from django.db import models

class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    phone_number = models.BigIntegerField()
    monthly_salary = models.PositiveIntegerField()
    approved_limit = models.PositiveIntegerField()
    

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Loan(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    
    loan_id = models.AutoField(primary_key=True)
    loan_amount = models.FloatField()
    tenure = models.PositiveIntegerField()
    interest_rate = models.FloatField()
    monthly_repayment = models.FloatField()
    emis_paid_on_time = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Loan {self.loan_id} - {self.customer_id.first_name} {self.customer_id.last_name}"
