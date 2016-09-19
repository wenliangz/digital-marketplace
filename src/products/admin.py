from django.contrib import admin

# Register your models here.
from .models import Product

class ProductModelAdmin(admin.ModelAdmin):
    list_display = ('title','description')
    class Meta:
        model = Product


admin.site.register(Product,ProductModelAdmin)