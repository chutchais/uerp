from django.forms import ModelForm

from .models import Po

class PoForm(ModelForm):
    class Meta:
        model = Po
        fields = '__all__'