from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.db.models import Sum
# from django.db.models import Sum

# Create your models here.
from product.models import ProductGroup

class Machine(models.Model):
	name 			= models.CharField(primary_key=True,max_length=50,null = False)
	slug 			= models.SlugField(unique=True,blank=True, null=True)
	description 	= models.TextField(null = True,blank = True)

	productgroup	= models.ForeignKey(ProductGroup,
							blank=True,null=True,
							on_delete=models.SET_NULL,
							related_name = 'machines')

	created_date	= models.DateTimeField(auto_now_add=True)
	modified_date	= models.DateTimeField(blank=True, null=True,auto_now=True)
	draft			= models.BooleanField(default=True)
	active			= models.BooleanField(default=True)


	def __str__(self):
		return ('%s' % self.name)

def create_machine_slug(instance, new_slug=None):
    slug = slugify(instance.name)
    if new_slug is not None:
        slug = new_slug
    qs = Machine.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.count())
        return create_machine_slug(instance, new_slug=new_slug)
    return slug

def pre_save_machine_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_machine_slug(instance)

pre_save.connect(pre_save_machine_receiver, sender=Machine)