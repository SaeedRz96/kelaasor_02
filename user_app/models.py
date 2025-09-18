from django.db import models
from django.contrib.auth.models import User


class UserWallet(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    amount = models.PositiveBigIntegerField(default=0)


class LoanRequest(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.PROTECT)
    amount = models.PositiveBigIntegerField()
    months = models.PositiveIntegerField()
    status = models.CharField(
        choices=[
            ('a','Approved'),
            ('r','Rejected'),
            ('p','Pending')
        ],
        max_length=1
    )
    request_date = models.DateTimeField(auto_now_add=True)
    

class Installment(models.Model):
    loan = models.ForeignKey(to=LoanRequest, on_delete=models.PROTECT)
    date = models.DateField()
    amount = models.PositiveBigIntegerField()
    