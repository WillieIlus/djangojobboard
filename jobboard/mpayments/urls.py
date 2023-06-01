from django.urls import path

from .views import MpesaCallbackView, InitiatePaymentView, TransactionListCreateView, TransactionRetrieveUpdateDestroyView

urlpatterns = [
    path('callback/', MpesaCallbackView.as_view(), name='mpesa-callback'),
    path('initiate-payment/', InitiatePaymentView.as_view(), name='mpesa-initiate-payment'),
    path('transactions/', TransactionListCreateView.as_view(), name='transaction-list-create'),
    path('transactions/<int:pk>/', TransactionRetrieveUpdateDestroyView.as_view(), name='transaction-retrieve-update-destroy'),
]
