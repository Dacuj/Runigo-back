from django.urls import path
from .views import *

urlpatterns = [
    path('list', ProductListView.as_view(), name='home'),
    path('detail/<id>/', ProductDetailView.as_view(), name='detail'),
    path('success/', PaymentSuccessView.as_view(), name='success'),
    path('failed/', PaymentFailedView.as_view(), name='failed'),
    path('history/', OrderHistoryListView.as_view(), name='history'),

    path('api/checkout-session/<int:id>/', create_checkout_session, name='api_checkout_session'),

    path('create-checkout-session/' , CreateCheckoutSession.as_view()),  
    # path('webhook-test/' , WebHook.as_view()), 
]