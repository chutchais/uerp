from django.contrib import admin
from django.urls import path


from .views import index,DeliveryListView,DeliveryDetailView

urlpatterns = [
    path('', index, name='index'),
    path('list/', DeliveryListView.as_view(), name='list'),
    path('<int:pk>', DeliveryDetailView.as_view(), name='detail'),
]