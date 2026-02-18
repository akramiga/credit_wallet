from django.urls import path
from .views import CreditWalletView

urlpatterns = [
    path("wallets/<uuid:wallet_id>/credit/", CreditWalletView.as_view()),
]
