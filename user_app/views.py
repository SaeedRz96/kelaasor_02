from django.http.response import HttpResponse, JsonResponse
from django.utils.timezone import now
from datetime import timedelta
import json

from user_app.models import LoanRequest, Installment, UserWallet
from finance_app.models import Bank

from django.views.decorators.csrf import csrf_exempt

from rest_framework.generics import ListAPIView
from user_app.serializers import LoanRequestSerializer


def loan_request(request, user_id, amount, months):
    if months > 12:
        return HttpResponse("Max months is 12")
    if amount > 10000000:
        return HttpResponse("Max amount is 10000000")
    bank = Bank.objects.first()
    if amount > bank.amount:
        return HttpResponse("Request invalid")
    LoanRequest.objects.create(
        owner_id = user_id,
        amount = amount,
        months = months,
        status = 'p'
    )
    return HttpResponse("The loan request submited!")


@csrf_exempt
def loan_request_post(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data['user_id']
        amount = data['amount']
        months = data['months']
        if months > 12:
            return HttpResponse("Max months is 12")
        if amount > 10000000:
            return HttpResponse("Max amount is 10000000")
        bank = Bank.objects.first()
        if amount > bank.amount:
            return HttpResponse("Request invalid")
        LoanRequest.objects.create(
            owner_id = user_id,
            amount = amount,
            months = months,
            status = 'p'
        )
        return HttpResponse("The loan request submited!")
    else:
        return HttpResponse("Method not allowed")


def change_request_status(request, loan_id, status):
    if status not in ['p','a','r']:
        return HttpResponse("Status incorrect")
    loan = LoanRequest.objects.get(id=loan_id)
    loan.status = status
    loan.save()
    if loan.status == 'a':
        for i in range(1, loan.months+1):
            Installment.objects.create(
                loan = loan,
                date = now() + timedelta(days = 30 * i),
                amount = loan.amount / loan.months
            )
        wallet = UserWallet.objects.get(owner=loan.owner)
        wallet.amount = wallet.amount + loan.amount
        wallet.save()
        bank = Bank.objects.first()
        bank.amount = bank.amount - loan.amount
        bank.save()
    return HttpResponse("Loan request status changed")


@csrf_exempt
def delete_loan_request(request, loan_id):
    if request.method == 'DELETE':
        loan = LoanRequest.objects.get(id=loan_id)
        if loan.status == 'p':
            loan.delete()
        return HttpResponse("Loan deleted!")


def loan_request_list(request):
    loan_requests = LoanRequest.objects.all().values("owner","amount","months")
    loan_requests = list(loan_requests)
    return JsonResponse(loan_requests, safe=False)


class LoanRequestList(ListAPIView):
    queryset = LoanRequest.objects.all()
    serializer_class = LoanRequestSerializer