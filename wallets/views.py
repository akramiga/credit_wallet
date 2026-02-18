from decimal import Decimal
from django.db import transaction, IntegrityError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Wallet, WalletLedger
from .serializers import CreditSerializer
from .permissions import IsOpsOrParent


class CreditWalletView(APIView):
    permission_classes = [IsOpsOrParent]

    def post(self, request, wallet_id):
        serializer = CreditSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        amount = serializer.validated_data["amount"]
        currency = serializer.validated_data.get("currency", "UGX")
        idempotency_key = serializer.validated_data["idempotency_key"]
        reference = serializer.validated_data.get("reference")
        metadata = serializer.validated_data.get("metadata")

        with transaction.atomic():
            wallet = Wallet.objects.select_for_update().get(id=wallet_id)

            if wallet.currency != currency:
                return Response(...)

            try:
                with transaction.atomic():
                    ledger = WalletLedger.objects.create(
                        wallet=wallet,
                        entry_type=WalletLedger.EntryType.CREDIT,
                        amount=amount,
                        idempotency_key=idempotency_key,
                        reference=reference,
                        metadata=metadata
                    )
                    created = True
            except IntegrityError:
                created = False

            if created:
                wallet.balance += amount
                wallet.save()
                http_status = status.HTTP_201_CREATED
            else:
                ledger = WalletLedger.objects.get(
                    wallet=wallet,
                    idempotency_key=idempotency_key
                )
                http_status = status.HTTP_200_OK
        return Response(
        {
            "wallet_id": str(wallet.id),
            "ledger_entry_id": ledger.id,
            "credited_amount": str(ledger.amount),
            "currency": wallet.currency,
            "new_balance": str(wallet.balance),
            "status": "SUCCESS"
        },
        status=http_status
    )