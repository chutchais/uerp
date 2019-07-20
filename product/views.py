from django.shortcuts import render
from django.db.models import Q,F
from django.views.generic import View,ListView,DetailView,CreateView,UpdateView,DeleteView


from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
# Create your views here.
import datetime

@login_required
@permission_required('product.can_view')
def index(request):
    fname = "product/index.html"
    product_list = Product.objects.filter(
    					active = True,modified_date__gt= datetime.datetime.today()-datetime.timedelta(days=30)
    					).order_by('group','name')
    return render(
			request,
			fname,
			{
				'object_list' : product_list
			}
		)

from .models import Product,ProductGroup

class ProductListView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
	model = Product
	paginate_by = 100
	permission_required = ('product.can_view','product.can_edit','product.can_add')

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

class ProductDetailView(LoginRequiredMixin,PermissionRequiredMixin,DetailView):
	model = Product
	permission_required = ('product.can_view','product.can_edit','product.can_add')


class ProductGroupListView(LoginRequiredMixin,ListView):
	model = ProductGroup

class ProductGroupDetailView(LoginRequiredMixin,DetailView):
	model = ProductGroup