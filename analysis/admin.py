from django.contrib import admin

from .models import JewelryInventory, JewelrySales

admin.site.register(JewelrySales)
admin.site.register(JewelryInventory)
