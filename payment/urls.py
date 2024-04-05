from django.urls import path
from .views import payment,paymentHandler

urlpatterns = [
    path('payment',payment.as_view(),name='payment'),
    path('paymenthandler',paymentHandler.as_view(),name='payment_handler')
]
