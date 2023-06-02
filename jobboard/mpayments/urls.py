# from django.urls import path
#
# from .views import mpesa_callback_view, initiate_payment_view, TransactionListCreateView, TransactionRetrieveUpdateDestroyView, index
#
# urlpatterns = [
#     path('callback/', mpesa_callback_view, name='mpesa-callback'),
#     path('initiate-payment/', initiate_payment_view, name='mpesa-initiate-payment'),
#     path('transactions/', TransactionListCreateView.as_view(), name='transaction-list-create'),
#     path('transactions/<int:pk>/', TransactionRetrieveUpdateDestroyView.as_view(), name='transaction-retrieve-update-destroy'),
#     path('', index, name='index'),
# ]
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('callback/', views.mpesa_callback_view, name='mpesa-callback'),
    path('initiate-payment/', views.initiate_payment_view, name='initiate-payment'),
]
