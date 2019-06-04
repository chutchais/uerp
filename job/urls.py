from django.contrib import admin
from django.urls import path


from .views import (JobListView,JobDetailView,JobDeleteView,
					update_recipe,reset_recipe,update_job_finished,
					add_job_complete,delete_job_complete,
                    add_job_inspection,delete_job_inspection,index)

urlpatterns = [
    path('', index, name='index'),
    path('list/', JobListView.as_view(), name='list'),
    path('<slug:slug>', JobDetailView.as_view(), name='detail'),
    path('<slug:slug>/delete', JobDeleteView.as_view(), name='delete'),
    path('<slug:slug>/finish', update_job_finished, name='recipe-finish'),
    path('<slug:slug>/recipe', update_recipe, name='recipe-update'),
    path('<slug:slug>/recipe/reset', reset_recipe, name='recipe-reset'),
    path('<slug:slug>/complete/add', add_job_complete, name='complete-add'),
    path('<slug:slug>/complete/<int:pk>/delete', delete_job_complete, name='complete-delete'),
    path('<slug:slug>/inspect/add', add_job_inspection, name='inspect-add'),
    path('<slug:slug>/inspect/delete', delete_job_inspection, name='inspect-delete'),
]
