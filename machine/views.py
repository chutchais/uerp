from django.shortcuts import render
from django.db.models import Q,F
from django.views.generic import View,ListView,DetailView,CreateView,UpdateView,DeleteView
from django.http import HttpResponse,HttpResponseRedirect

# Create your views here.
from .models import Machine
class MachineListView(ListView):
	model 		= Machine
	paginate_by = 100

	def get_queryset(self):
		query = self.request.GET.get('q')
		if query :
			return Machine.objects.filter(Q(name__icontains=query) |
									Q(description__icontains=query)).order_by('-created_date')
		return Machine.objects.all()

class MachineDetailView(DetailView):
	model = Machine

def index(request):
    fname = "Machine/index.html"
    return render(
			request,
			fname
		)
