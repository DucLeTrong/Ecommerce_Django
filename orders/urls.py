from django.urls import path
from . import views


urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    path('payments/', views.payments, name='payments'),
    path('make_payment/', views.make_payment, name='make_payment'),
    path('order_complete/<str:order_number>/<str:trans_id>/', views.order_completed, name='order_complete'),
]
