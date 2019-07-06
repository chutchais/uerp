from django.shortcuts import render
from django.db.models import Q,F
from django.views.generic import View,ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

@login_required
def index(request):
    fname = "product/index.html"
    return render(
			request,
			fname
		)

from .models import Product,ProductGroup

class ProductListView(LoginRequiredMixin,ListView):
	model = Product
	paginate_by = 100

	def get_queryset(self):
		query = self.request.GET.get('q')
		if query :
			return Product.objects.filter(Q(name__icontains=query) |
									Q(fg_name__icontains=query) |
									Q(description__icontains=query) |
									Q(customer__name__icontains=query)|
									Q(parent__name__icontains=query) |
									Q(group__name__icontains=query) ).order_by('-created_date')
		return Product.objects.all()

class ProductDetailView(LoginRequiredMixin,DetailView):
	model = Product


class ProductGroupListView(LoginRequiredMixin,ListView):
	model = ProductGroup

class ProductGroupDetailView(LoginRequiredMixin,DetailView):
	model = ProductGroup