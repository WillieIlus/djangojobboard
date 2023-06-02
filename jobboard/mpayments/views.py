import json
import logging

from django.http import HttpResponse
from django_daraja.mpesa.core import MpesaClient

from .models import Transaction
from .serializers import TransactionSerializer

logger = logging.getLogger(__name__)



def mpesa_callback_view(request):
    logger.info("Callback from MPESA")
    data = request.POST
    status_code = check_status(data)
    transaction = get_or_create_transaction(data)

    if status_code == 0:
        handle_successful_payment(data, transaction)
    else:
        transaction.status = 1

    transaction.save()
    transaction_data = TransactionSerializer(transaction).data

    logger.info("Transaction completed info: {}".format(transaction_data))

    return HttpResponse('{"status": "ok", "code": 0}')




def initiate_payment_view(request):
    cl = MpesaClient()
    phone_number = '0705482738'
    amount = 1
    account_reference = 'reference'
    transaction_desc = 'description'
    callback_url = 'https://willieilus.pythonanywhere.com/pay/callback'
    response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
    return HttpResponse(response)


def index(request):
    cl = MpesaClient()
    phone_number = '0705482738'
    amount = 1
    account_reference = 'reference'
    transaction_desc = 'Description'
    callback_url = 'https://willieilus.pythonanywhere.com/pay/callback'
    response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
    return HttpResponse(response)



def check_status(data):
    try:
        status_code = int(data["Body"]["stkCallback"]["ResultCode"])
    except Exception as e:
        logger.error(f"Error: {e}")
        status_code = 1
    return status_code


def handle_successful_payment(data, transaction):
    items = data["Body"]["stkCallback"]["CallbackMetadata"]["Item"]
    for item in items:
        if item["Name"] == "Amount":
            transaction.amount = item["Value"]
        elif item["Name"] == "MpesaReceiptNumber":
            transaction.receipt_no = item["Value"]
        elif item["Name"] == "PhoneNumber":
            transaction.phone_number = item["Value"]

    transaction.confirmed = True


def get_or_create_transaction(data):
    transaction_id = data["Body"]["stkCallback"]["CheckoutRequestID"]
    transaction, created = Transaction.objects.get_or_create(transaction_id=transaction_id)
    return transaction
