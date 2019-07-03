from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.db.models.signals import pre_save

# Create your models here.
class Customer(models.Model):
	name 				= models.CharField(primary_key=True,max_length=50,null = False)
	slug 				= models.SlugField(unique=True,blank=True, null=True)
	description 		= models.TextField(null = True,blank = True)
	address				= models.TextField(null = True,blank = True)
	delivery_address	= models.TextField(null = True,blank = True)
	tax					= models.CharField(max_length=50,null = True,blank = True )
	created_date		= models.DateTimeField(auto_now_add=True)
	modified_date		= models.DateTimeField(blank=True, null=True,auto_now=True)
	active				= models.BooleanField(default=True)

	class Meta:
		verbose_name = 'Customer'
		verbose_name_plural = 'Customer (Master Data)'

	def __str__(self):
		return ('%s' % self.name)

	def get_absolute_url(self):
		# return 'test'
		return reverse('customer:detail', kwargs={'slug': self.slug})

def pre_save_customer_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)

pre_save.connect(pre_save_customer_receiver, sender= Customer)


class Contact(models.Model):
	name 				= models.CharField(max_length=100,null = True,blank = True)
	customer 			= models.ForeignKey(Customer,
							blank=True,null=True,
							on_delete=models.CASCADE,
							related_name = 'contacts')
	position			= models.CharField(max_length=50,null = True,blank = True )
	mobile 				= models.CharField(max_length=50,null = True,blank = True )
	telephone 			= models.CharField(max_length=50,null = True,blank = True )
	email				= models.EmailField()
	created_date		= models.DateTimeField(auto_now_add=True)
	modified_date		= models.DateTimeField(blank=True, null=True,auto_now=True)
	active				= models.BooleanField(default=True)

	def __str__(self):
		return ('%s' % self.name)

	# def get_absolute_url(self):
	# 	# return 'test'
	# 	return reverse('customer:detail', kwargs={'slug': self.slug})