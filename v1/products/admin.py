# -*- coding: utf-8 -*-
from django.contrib import admin

from .models.product import Product
from .models.product_image import ProductImage

admin.site.register(Product)
admin.site.register(ProductImage)
