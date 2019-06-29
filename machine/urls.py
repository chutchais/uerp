from django.contrib import admin
from django.urls import path


from .views import index,MachineListView,MachineDetailView

urlpatterns = [
    path('', index, name='index'),
    path('list/', MachineListView.as_view(), name='list'),
    path('<slug:slug>', MachineDetailView.as_view(), name='detail'),
]
