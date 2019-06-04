from django.shortcuts import render
from django.views.generic import View,ListView,DetailView,CreateView,UpdateView,DeleteView

# Create your views here.

def index(request):
    fname = "product/index.html"
    return render(
			request,
			fname
		)

from .models import Product,ProductGroup
class ProductListView(ListView):
	model = Product

class ProductDetailView(DetailView):
	model = Product


class ProductGroupListView(ListView):
	model = ProductGroup

class ProductGroupDetailView(DetailView):
	model = ProductGroup