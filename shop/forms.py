from django import forms
from .models import Category

class ItemForm(forms.Form):
    name = forms.CharField()
    slug = forms.SlugField()
    category = forms.ChoiceField(choices=[(x, x.name) for x in Category.objects.all()])
    description = forms.CharField(widget=forms.Textarea)
    price = forms.DecimalField()
    stock = forms.IntegerField()
    main_image = forms.ImageField()

class AddImageForm(forms.Form):
    image = forms.ImageField()