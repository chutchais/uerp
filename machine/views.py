from django.shortcuts import render
from django.db.models import Q,F
from django.views.generic import View,ListView,DetailView,CreateView,UpdateView,DeleteView
from django.http import HttpResponse,HttpResponseRedirect

from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin

 

# Create your views here.
from .models import Machine

@login_required
@permission_required('machine.view_machine')
def index(request):
    fname = "machine/index.html"
    machine_list = Machine.objects.select_related('productgroup').filter(
    					active = True
    					).order_by('productgroup','name')
    return render(
			request,
			fname,
			{
				'object_list' : machine_list
			}
		)

class MachineListView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
	# model 		= Machine
	queryset 	= Machine.objects.select_related()
	paginate_by = 100
	permission_required = ('machine.view_machine')

	def get_queryset(self):
		query = self.request.GET.get('q')
		if query :
			return Machine.objects.select_related('productgroup').filter(Q(name__icontains=query) |
									Q(description__icontains=query)).order_by('-created_date')
		return Machine.objects.select_related()

class MachineDetailView(LoginRequiredMixin,PermissionRequiredMixin,DetailView):
	# model = Machine
	queryset 	= Machine.objects.select_related()
	permission_required = ('machine.view_machine')


