from django.contrib import admin
from django.urls import path


from .views import CustomerListView,CustomerDetailView,index

urlpatterns = [
    path('', index, name='index'),
    path('list/', CustomerListView.as_view(), name='list'),
    path('<slug:slug>', CustomerDetailView.as_view(), name='detail'),
]
