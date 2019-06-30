from django.db import models
from django.shortcuts import reverse

class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:list', args=[self.slug])

class Item(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default="Item", null=False, blank=False, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True)
    description = models.TextField(null=False, blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    seller = models.ForeignKey('userm.UserExtendedR', on_delete=models.CASCADE)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("shop:detail", args=[self.pk, self.slug])
    

class Photo(models.Model):
    photo = models.ImageField(upload_to='shop/', blank=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)