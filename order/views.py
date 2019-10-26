from django.shortcuts import render
from django.db.models import Q,F
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.views.generic import View,ListView,DetailView,CreateView,UpdateView,DeleteView
from datetime import datetime

from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin

# Create your views here.
from .models import Order,OrderItem
from job.models import Job
from po.models import Po

@login_required
@permission_required('order.view_order')
def index(request):
    fname = "order/index.html"
    order_list 	= Order.objects.select_related('product__group').filter(
    						active= True ,
    						completed = False
    					).order_by('product__group','created_date')
    return render(
			request,
			fname,
			{
				'object_list' : order_list
			}
		)

class OrderListView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
	# model = Order
	queryset = Order.objects.select_related()
	paginate_by = 100
	permission_required = ('order.view_order')

	def get_queryset(self):
		query = self.request.GET.get('q')
		if query :
			# print(query)
			return Order.objects.filter(Q(name__icontains=query) |
									Q(description__icontains=query) |
									Q(product__name__icontains=query)|
									Q(product__fg_name__icontains=query)|
									Q(product__description__icontains=query)).order_by('-created_date')
		return Order.objects.select_related()


class OrderDetailView(LoginRequiredMixin,PermissionRequiredMixin,DetailView):
	# model = Order
	queryset = Order.objects.select_related()
	permission_required = ( 'order.view_order')

	def get_context_data(self, **kwargs):
		context     		= super().get_context_data(**kwargs)
		order 				= self.get_object()
		context['po_list'] 	= Po.objects.filter(product = order.product,
												active=True,started=False).order_by('created_date')
		return context


class OrderItemCreateView(LoginRequiredMixin,CreateView):
	# model = OrderItem
	queryset = OrderItem.objects.select_related()

class OrderItemListView(LoginRequiredMixin,ListView):
	# model = OrderItem
	queryset = OrderItem.objects.select_related()

class OrderItemDeleteView(LoginRequiredMixin,DeleteView):
	# model = OrderItem
	queryset = OrderItem.objects.select_related()
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

@login_required
def add_order_item(requets,slug):
	order 	= Order.objects.get(slug=slug)
	po 		= Po.objects.get(slug=requets.POST.get('po'))
	OrderItem.objects.create(order=order,
					 po=po)
	po.active=False
	po.save()
	return HttpResponseRedirect(reverse('order:detail',kwargs={ 'slug': slug }))

# @login_required
def get_job_seq(year,month,product_group):
	job = Job.objects.filter(product__group = product_group,
							created_date__year = year,
							created_date__month = month)
	# print (year,month,product_group)
	return '{:03}'.format(job.count()+1)

# @login_required
def create_job(request,slug):
	order = Order.objects.get(slug=slug)
	print ('Create job of Order %s' % slug)

	# Must create master job First
	# ----------------------------


	# if order.product.products.count() == 0: #Single/Master Job
	# 	# job_name = '%s_%s' % (order.slug,order.product.slug)
	# 	product_group = order.product.group.name if order.product.group else 'XX'
	# 	job_prefix = order.product.job_prefix if order.product.job_prefix else 'JC%s' % product_group
	# 	job_name = '%s%s-%s' % (job_prefix,datetime.now().strftime('%y%m'),
	# 						get_job_seq(datetime.now().year,datetime.now().month,order.product.group))
	# 	job,created = Job.objects.get_or_create(name=job_name,
	# 										description=order.description,
	# 										product=order.product,
	# 										order=order,
	# 										qty=order.qty())
	# else:
	# # Case FG product has Semi part
	# 	for part in order.product.products.all():
	# 		product_group = part.group.name if part.group else 'XX'
	# 		job_prefix = order.product.job_prefix if order.product.job_prefix else 'JC%s' % product_group
	# 		job_name = '%s%s-%s' % (job_prefix,datetime.now().strftime('%y%m'),
	# 						get_job_seq(datetime.now().year,datetime.now().month,part.group))


	# 		job,created = Job.objects.get_or_create(name=job_name,
	# 										description=order.description,
	# 										product=part,
	# 										order=order,
	# 										qty=order.qty())

	# Single Or Master Job
	product_group = order.product.group.name if order.product.group else 'XX'
	job_prefix = order.product.job_prefix if order.product.job_prefix else 'JC%s' % product_group
	job_name = '%s%s-%s' % (job_prefix,datetime.now().strftime('%y%m'),
						get_job_seq(datetime.now().year,datetime.now().month,order.product.group))
	master_job,created = Job.objects.get_or_create(name=job_name,
										description=order.description,
										product=order.product,
										order=order,
										qty=order.qty())
	
	if order.product.products.count() > 0:
		master_job.master = True
		master_job.save()
	# Case FG product has Semi part
		for part in order.product.products.all():
			product_group = part.group.name if part.group else 'XX'
			job_prefix = order.product.job_prefix if order.product.job_prefix else 'JC%s' % product_group
			job_name = '%s%s-%s' % (job_prefix,datetime.now().strftime('%y%m'),
							get_job_seq(datetime.now().year,datetime.now().month,part.group))


			job,created = Job.objects.get_or_create(name=job_name,
											description=order.description,
											product=part,
											order=order,
											qty=order.qty(),
											parent=master_job)
			# print (job_name,created)

	for item in order.orderitems.all().order_by('seq'):
		po = item.po
		po.started = True
		po.save()
	print ('Update Order draft to False')
	order.draft = False
	order.save()


	return HttpResponseRedirect(reverse('order:detail',kwargs={ 'slug': slug }))

# @login_required
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

	order.draft = True
	order.save()




	return HttpResponseRedirect(reverse('order:detail',kwargs={ 'slug': slug }))