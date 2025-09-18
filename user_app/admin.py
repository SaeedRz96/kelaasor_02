from django.contrib import admin
from user_app.models import UserWallet, LoanRequest, Installment

admin.site.register(UserWallet)
admin.site.register(LoanRequest)
admin.site.register(Installment)