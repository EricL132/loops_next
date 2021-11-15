from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingInfo)
admin.site.register(Featured)
admin.site.register(Coupons)
admin.site.register(TempOrder)
admin.site.register(ResetToken)