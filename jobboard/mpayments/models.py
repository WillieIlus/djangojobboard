import uuid

STATUS = ((1, "Pending"), (0, "Complete"))

from django.db import models


class PaymentResponse(models.Model):
    merchant_request_id = models.CharField(max_length=100)
    checkout_request_id = models.CharField(max_length=100)
    response_code = models.CharField(max_length=10)
    response_description = models.CharField(max_length=200)
    customer_message = models.CharField(max_length=200)

    def __str__(self):
        return self.merchant_request_id


class Transaction(models.Model):
    transaction_no = models.CharField(default=uuid.uuid4, max_length=50, unique=True)
    phone_number = models.IntegerField(null=False, blank=False)
    checkout_request_id = models.CharField(max_length=200)
    reference = models.CharField(max_length=40, blank=True)
    description = models.TextField(null=True, blank=True)
    amount = models.CharField(max_length=10)
    status = models.CharField(max_length=15, choices=STATUS, default=1)
    receipt_no = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    ip = models.CharField(max_length=200, blank=True, null=True)

    def __unicode__(self):
        return f"{self.transaction_no}"
