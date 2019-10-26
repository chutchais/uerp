from django.shortcuts import render
from django.db.models import Q,F
from django.views.generic import View,ListView,DetailView,CreateView,UpdateView,DeleteView
from django.http import HttpResponse,HttpResponseRedirect


from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin

# Create your views here.
from .models import Po
from product.models import ProductGroup

@login_required
@permission_required('po.view_po')
def index(request):
    fname = "po/index.html"
    po_list 	= Po.objects.select_related('product__group').filter(
    						active= True ,
    						completed = False
    					).order_by('product__group','created_date')
    return render(
			request,
			fname,
			{
				'po_list' : po_list
			}
		)

class PoListView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
	# model 		= Po
	queryset 	= Po.objects.select_related()
	paginate_by = 100
	permission_required = ('po.view_po')

	def get_queryset(self):
		query = self.request.GET.get('q')
		if query :
			return Po.objects.select_related('product').filter(Q(name__icontains=query) |
									Q(description__icontains=query) |
									Q(product__name__icontains=query)|
									Q(product__fg_name__icontains=query)|
									Q(product__description__icontains=query)).order_by('-modified_date')
		return Po.objects.select_related()

class PoDetailView(LoginRequiredMixin,PermissionRequiredMixin,DetailView):
	# model = Po
	queryset 	= Po.objects.select_related()
	permission_required = ('po.view_po')


