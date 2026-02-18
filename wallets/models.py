import uuid
from decimal import Decimal
from django.db import models
from django.db.models import Q


class Wallet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    currency = models.CharField(max_length=10, default="UGX")
    balance = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        default=Decimal("0.00")
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} - {self.balance} {self.currency}"


class WalletLedger(models.Model):

    class EntryType(models.TextChoices):
        CREDIT = "CREDIT", "Credit"

    wallet = models.ForeignKey(
        Wallet,
        on_delete=models.CASCADE,
        related_name="ledger_entries"
    )

    entry_type = models.CharField(
        max_length=20,
        choices=EntryType.choices,
        default=EntryType.CREDIT
    )

    amount = models.DecimalField(
        max_digits=18,
        decimal_places=2
    )

    idempotency_key = models.CharField(max_length=255)
    reference = models.CharField(max_length=255, blank=True, null=True)
    metadata = models.JSONField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["wallet", "idempotency_key"],
                name="unique_wallet_idempotency"
            ),
            models.CheckConstraint(
                check=Q(amount__gt=0),
                name="amount_gt_zero"
            )
        ]

    def __str__(self):
        return f"{self.wallet_id} - {self.amount}"

