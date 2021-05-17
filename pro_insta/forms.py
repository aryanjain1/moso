from django import forms
from .models import insta







class Insta_Form(forms.Form):
    m = insta.objects.values('city',).distinct()
    m1 = insta.objects.values('category').distinct()

    city = forms.CharField(label='City', widget=forms.Select(choices=m))
    category = forms.CharField(label='Category', widget=forms.CheckboxSelectMultiple(choices=m1))


