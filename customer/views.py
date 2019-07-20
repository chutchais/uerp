from django.shortcuts import render
from django.db.models import Q,F
from django.views.generic import View,ListView,DetailView,CreateView,UpdateView,DeleteView

from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
# Create your views here.
from .models import Customer

@login_required
@permission_required('customer.can_view')
def index(request):
    fname = "customer/index.html"
    return render(
			request,
			fname
		)

class CustomerListView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
	model = Customer
	paginate_by = 100
	permission_required = ('customer.can_view','customer.can_edit','customer.can_add')

	def get_queryset(self):
		query = self.request.GET.get('q')
		if query :
			return Customer.objects.filter(Q(name__icontains=query) |
									Q(description__icontains=query) |
									Q(address__icontains=query) |
									Q(delivery_address__icontains=query) |
									Q(tax__icontains=query)).order_by('-created_date')
		return Customer.objects.all()

class CustomerDetailView(LoginRequiredMixin,PermissionRequiredMixin,DetailView):
	model = Customer
	permission_required = ('customer.can_view','customer.can_edit','customer.can_add')


# permission_required = 'polls.can_vote'
#     # Or multiple of permissions:
# permission_required = ('polls.can_open', 'polls.can_edit')