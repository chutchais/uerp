from django.contrib import admin
from django.urls import path


from .views import (OrderListView,OrderDetailView,create_job,delete_job,
					OrderItemListView,
					OrderItemDeleteView,
					OrderItemCreateView,add_order_item,index)

urlpatterns = [
    path('', index, name='index'),
    path('list/', OrderListView.as_view(), name='list'),
    path('<slug:slug>', OrderDetailView.as_view(), name='detail'),
    path('<slug:slug>/create_job', create_job, name='create-job'),
    path('<slug:slug>/delete_job', delete_job, name='delete-job'),
    path('<slug:slug>/items/add', add_order_item, name='create-item'),
    path('items/', OrderItemListView.as_view(), name='items'),
    path('items/<int:pk>/delete', OrderItemDeleteView.as_view(), name='items-delete'),
]
