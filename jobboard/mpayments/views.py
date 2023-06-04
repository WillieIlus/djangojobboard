import logging
import time

from django.shortcuts import redirect
from requests.auth import HTTPBasicAuth

from .models import PaymentResponse

logger = logging.getLogger(__name__)

import base64
from datetime import datetime
import json

import requests
from django.http import HttpResponse
from django_daraja.mpesa.core import MpesaClient

consumer_key = "lOIGknrirnapyrzdKp5VavouJ6ABy0RR"
consumer_secret = "bMV32BQqTemWtGHA"
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
shortcode = 174379
pass_key = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
access_token_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
checkout_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
transaction_status_url = "https://sandbox.safaricom.co.ke/mpesa/transactionstatus/v1/query"


def generate_password():
    password_str = str(shortcode) + str(pass_key) + str(timestamp)
    password_bytes = password_str.encode("ascii")
    return base64.b64encode(password_bytes).decode("utf-8")


def get_access_token(request):
    response = requests.get(access_token_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(response.text)
    validated_mpesa_access_token = mpesa_access_token["access_token"]
    return validated_mpesa_access_token


def initiate_payment_view(request):
    cl = MpesaClient()
    phone_number = "0705482738"
    amount = 1
    account_reference = "reference"
    transaction_desc = "description"
    callback_url = "https://willieilus.pythonanywhere.com/pay/callback"
    response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)

    payment_response = PaymentResponse.objects.create(
        merchant_request_id=response.merchant_request_id,
        checkout_request_id=response.checkout_request_id,
        response_code=response.response_code,
        response_description=response.response_description,
        customer_message=response.customer_message
    )

    time.sleep(15)  # Pause execution for 1 minute (60 seconds)

    return redirect("check_payment", checkout_request_id=payment_response.checkout_request_id)

    # return HttpResponse(response)


def check_payment(request, checkout_request_id):
    cl = MpesaClient()
    access_token = cl.access_token()
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer %s' % access_token
    }

    payload = {
        "BusinessShortCode": 174379,
        "Password": "MTc0Mzc5YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMjMwNjAzMjM0MjE1",
        "Timestamp": "20230603234215",
        "CheckoutRequestID": checkout_request_id,
    }

    response = requests.post('https://sandbox.safaricom.co.ke/mpesa/stkpushquery/v1/query', headers=headers,
                             json=payload)

    result = response.json()
    result_code = result.get('ResultCode')
    result_desc = result.get('ResultDesc')

    if result_code == "0":
        result_text = "Success: " + result_desc
    else:
        result_text = "Error: " + result_desc

    return HttpResponse(result_text)


def mpesa_callback_view(request):
    pass
