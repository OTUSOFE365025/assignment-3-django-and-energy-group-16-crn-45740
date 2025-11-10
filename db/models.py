import sys

try:
    from django.db import models
except Exception:
    print('Exception: Django Not Found, please install it with "pip install django".')
    sys.exit()


# Product model
class Product(models.Model):
    upc = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=120)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        # Match A2 Display formatting: "UPC name $price"
        return f"{self.upc} {self.name} ${self.price:.2f}"
