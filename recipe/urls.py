from django.contrib import admin
from django.urls import path


from .views import RecipeListView,RecipeDetailView,index

urlpatterns = [
	path('', index, name='index'),
    path('list/', RecipeListView.as_view(), name='list'),
    path('<slug:slug>', RecipeDetailView.as_view(), name='detail'),
]
