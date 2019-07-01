from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.utils import timezone

# Create your models here.
from product.models import ProductGroup

DOWNTIME			=	'DOWNTIME'
MC_OPEN				=	'MC_OPEN'
CHG_MODEL			= 	'CHG_MODEL'
LOGO 				=   'CHG_LOGO'
DOWNTIME_TYPE_CHOICE = (
		(DOWNTIME,'Downtime'),
		(MC_OPEN,'Setup Open Machine'),
		(CHG_MODEL,'Change Model'),
		(LOGO,'Change Logo')
	)

class Downtime(models.Model):
	name 			= models.CharField(primary_key=True,max_length=50,null = False)
	slug 			= models.SlugField(unique=True,blank=True, null=True)
	description 	= models.TextField(null = True,blank = True)
	downtime_type 	= models.CharField(max_length=20,choices=DOWNTIME_TYPE_CHOICE,default=DOWNTIME)
	productgroup	= models.ForeignKey(ProductGroup,
							blank=True,null=True,
							on_delete=models.CASCADE,
							related_name = 'downtimes')
	created_date	= models.DateTimeField(auto_now_add=True)
	modified_date	= models.DateTimeField(blank=True, null=True,auto_now=True)
	active			= models.BooleanField(default=True)


	def __str__(self):
		return ('%s' % (self.name))


def create_downtime_slug(instance, new_slug=None):
	slug = slugify(instance.name)
	if new_slug is not None:
		slug = new_slug
	qs = Downtime.objects.filter(slug=slug)
	exists = qs.exists()
	if exists:
		new_slug = "%s-%s" %(slug, instance.productgroup)
		return create_downtime_slug(instance, new_slug=new_slug)
	return slug

def pre_save_downtime_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_downtime_slug(instance)

pre_save.connect(pre_save_downtime_receiver, sender=Downtime)
