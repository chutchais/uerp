from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.db.models import Sum

# Create your models here.
from customer.models import Customer
from product.models import Product

class Po(models.Model):
	name 			= models.CharField(primary_key=True,max_length=50,null = False)
	slug 			= models.SlugField(unique=True,blank=True, null=True)
	description 	= models.TextField(null = True,blank = True)
	qty				= models.IntegerField(default=0)
	customer		= models.ForeignKey(Customer,
							blank=True,null=True,
							on_delete=models.SET_NULL,
							related_name = 'pos')
	product			= models.ForeignKey(Product,
							blank=True,null=True,
							on_delete=models.SET_NULL,
							related_name = 'pos')
	delivery_date	= models.DateTimeField(blank=True, null=True)
	delivery_address= models.TextField(null = True,blank = True)
	created_date	= models.DateTimeField(auto_now_add=True)
	modified_date	= models.DateTimeField(blank=True, null=True,auto_now=True)
	active			= models.BooleanField(default=True)
	started			= models.BooleanField(default=False)
	completed		= models.BooleanField(default=False)


	def __str__(self):
		return ('%s' % self.name)

	def order(self):
		return self.orderitems.order.name

	def weight(self):
		if self.product != None :
			return self.product.weight * self.qty
		return 0

	def weight_unit(self):
		if self.product != None :
			return self.product.weight_unit
		return ''

	def get_absolute_url(self):
		return reverse('po:detail', kwargs={'slug': self.slug})


	# def job(self):
	# 	return self.jobs.count()

	# def total(self):
	# 	return self.jobs.aggregate(Sum('qty'))['qty__sum']

def pre_save_po_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)

pre_save.connect(pre_save_po_receiver, sender=Po)