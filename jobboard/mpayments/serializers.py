from rest_framework import serializers

from .models import Transaction


class MpesaCheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = (
            "phone_number",
            "amount",
            "reference",
            "description",
        )


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"
