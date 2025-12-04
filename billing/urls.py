from django.urls import path

from .views import CreateCheckoutSessionView, ConfirmPaymentView


urlpatterns = [
    path('create-checkout-session/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('confirm-payment/', ConfirmPaymentView.as_view(), name='confirm-payment/'),
]
