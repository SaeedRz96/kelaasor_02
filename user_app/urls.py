from django.urls import path
from user_app.views import (
    loan_request,
    change_request_status,
    loan_request_post,
    delete_loan_request,
    loan_request_list,
    LoanRequestList
)


urlpatterns = [
    path("add-loan-request/<str:user_id>/<int:amount>/<int:months>", loan_request),
    path("change-request-status/<str:loan_id>/<str:status>", change_request_status),
    path("add-loan-request-post", loan_request_post),
    path("delete-loan/<str:loan_id>", delete_loan_request),
    path('loan-request-list', loan_request_list),
    path('loan-request-list2', LoanRequestList.as_view())
]
