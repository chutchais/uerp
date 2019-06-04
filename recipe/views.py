from django.shortcuts import render
from django.views.generic import View,ListView,DetailView,CreateView,UpdateView,DeleteView

# Create your views here.
from .models import Recipe

def index(request):
    fname = "recipe/index.html"
    return render(
			request,
			fname
		)

class RecipeListView(ListView):
	model = Recipe

class RecipeDetailView(DetailView):
	model = Recipe