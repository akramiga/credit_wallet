from decimal import Decimal
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from wallets.models import Wallet, WalletLedger


class CreditWalletTests(APITestCase):

    def setUp(self):
        self.wallet = Wallet.objects.create(currency="UGX")
        self.url = f"/wallets/{self.wallet.id}/credit/"
        self.headers = {"HTTP_X_ROLE": "OPS"}  # Django test client format

    # 1️⃣ Happy Path
    def test_credit_wallet_success(self):
        data = {
            "amount": "1000.00",
            "currency": "UGX",
            "idempotency_key": "abc-123"
        }

        response = self.client.post(self.url, data, format="json", **self.headers)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WalletLedger.objects.count(), 1)

        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.balance, Decimal("1000.00"))
        self.assertEqual(response.data["status"], "SUCCESS")

    # 2️⃣ Idempotency
    def test_idempotent_credit(self):
        data = {
            "amount": "1000.00",
            "currency": "UGX",
            "idempotency_key": "duplicate-key"
        }

        # First call
        response1 = self.client.post(self.url, data, format="json", **self.headers)

        # Second call (duplicate)
        response2 = self.client.post(self.url, data, format="json", **self.headers)

        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

        self.assertEqual(WalletLedger.objects.count(), 1)

        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.balance, Decimal("1000.00"))

    # 3️⃣ Validation - Reject zero or negative amount
    def test_reject_zero_amount(self):
        data = {
            "amount": "0.00",
            "currency": "UGX",
            "idempotency_key": "zero-test"
        }

        response = self.client.post(self.url, data, format="json", **self.headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reject_negative_amount(self):
        data = {
            "amount": "-100.00",
            "currency": "UGX",
            "idempotency_key": "negative-test"
        }

        response = self.client.post(self.url, data, format="json", **self.headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reject_missing_idempotency_key(self):
        data = {
            "amount": "1000.00",
            "currency": "UGX"
        }

        response = self.client.post(self.url, data, format="json", **self.headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # 4️⃣ RBAC
    def test_reject_missing_role(self):
        data = {
            "amount": "1000.00",
            "currency": "UGX",
            "idempotency_key": "role-test"
        }

        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_reject_invalid_role(self):
        data = {
            "amount": "1000.00",
            "currency": "UGX",
            "idempotency_key": "role-test"
        }

        response = self.client.post(
            self.url,
            data,
            format="json",
            HTTP_X_ACTOR_ROLE="USER"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

