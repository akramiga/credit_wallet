from rest_framework import serializers


class CreditSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=18, decimal_places=2)
    currency = serializers.CharField(required=False, default="UGX")
    idempotency_key = serializers.CharField()
    reference = serializers.CharField(required=False, allow_blank=True)
    metadata = serializers.JSONField(required=False)

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value
