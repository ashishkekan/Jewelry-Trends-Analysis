from django.db import models


class JewelrySales(models.Model):
    jewelry_code = models.CharField(max_length=50, unique=True)
    product_tags = models.TextField()
    sold_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.jewelry_code


class JewelryInventory(models.Model):
    jewelry_code = models.CharField(max_length=50, unique=True)
    product_tags = models.TextField()
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.jewelry_code
