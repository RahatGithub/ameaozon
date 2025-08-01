from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('process/<str:tracking_number>/', views.payment_process, name='payment_process'),
    path('complete/<str:tracking_number>/', views.payment_complete, name='payment_complete'),
    path('canceled/<str:tracking_number>/', views.payment_canceled, name='payment_canceled'),
]