from django.contrib import admin

from .models import Transaction, PaymentResponse

admin.site.register(Transaction)
admin.site.register(PaymentResponse)
