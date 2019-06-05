from django.shortcuts import render
from django.db.models import Q,F
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.views.generic import View,ListView,DetailView,CreateView,UpdateView,DeleteView

# Create your views here.
from .models import Order,OrderItem
from job.models import Job
from po.models import Po

def index(request):
    fname = "order/index.html"
    return render(
			request,
			fname
		)

class OrderListView(ListView):
	model = Order
	paginate_by = 100

	def get_queryset(self):
		query = self.request.GET.get('q')
		if query :
			return Order.objects.filter(Q(name__icontains=query) |
									Q(description__icontains=query) |
									Q(product__name__icontains=query)|
									Q(product__description__icontains=query)).order_by('-created_date')
		return Order.objects.all()


class OrderDetailView(DetailView):
	model = Order
	def get_context_data(self, **kwargs):
		context     		= super().get_context_data(**kwargs)
		order 				= self.get_object()
		context['po_list'] 	= Po.objects.filter(product = order.product,
												active=True,started=False).order_by('created_date')
		return context


class OrderItemCreateView(CreateView):
	model = OrderItem

class OrderItemListView(ListView):
	model = OrderItem

class OrderItemDeleteView(DeleteView):
	model = OrderItem
	def get_success_url(self):
		redirect = self.request.GET.get('next')
		return redirect

	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()
		po=self.object.po
		po.active=True
		po.save()
		return super(OrderItemDeleteView, self).delete(request, *args, **kwargs)
		# if can_delete:
  #           return super(EmployeeDeleteView, self).delete(
  #               request, *args, **kwargs)
  #       else:
  #           raise Http404("Object you are looking for doesn't exist")

def add_order_item(requets,slug):
	order 	= Order.objects.get(slug=slug)
	po 		= Po.objects.get(slug=requets.POST.get('po'))
	OrderItem.objects.create(order=order,
					 po=po)
	po.active=False
	po.save()
	return HttpResponseRedirect(reverse('order:detail',kwargs={ 'slug': slug }))

def create_job(request,slug):
	order = Order.objects.get(slug=slug)


	for part in order.product.products.all():
		# print( part.group.slug if part.group else 'none')
		job_name = '%s_%s_%s' % (part.group.slug if part.group else 'none',slug,part.slug)
		job,created = Job.objects.get_or_create(name=job_name,
										description=order.description,
										product=part,
										order=order,
										qty=order.qty())
		# print (job_name,created)

	for item in order.orderitems.all().order_by('seq'):
		po = item.po
		po.started = True
		po.save()

	return HttpResponseRedirect(reverse('order:detail',kwargs={ 'slug': slug }))

def delete_job(request,slug):
	order = Order.objects.get(slug=slug)
	ois = OrderItem.objects.filter(order=order)
	for oi in ois:
		po=oi.po
		print(po)
		po.started = False
		po.save()

	jobs = Job.objects.filter(order=order)
	for job in jobs:
		job.delete()



	return HttpResponseRedirect(reverse('order:detail',kwargs={ 'slug': slug }))