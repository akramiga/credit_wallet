from django.urls import path
from .views import CreditWalletView

urlpatterns = [
    path("wallets/<uuid:wallet_id>/credit/", CreditWalletView.as_view(), name="wallet-credit"),
    path("wallets/<int:wallet_id>/credit/", CreditWalletView.as_view())

]
