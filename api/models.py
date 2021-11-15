from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.utils.crypto import get_random_string
def randomProductID():
    while True:
        productID= get_random_string(8)
        productExistCheck = Product.objects.filter(productID=productID)
        if len(productExistCheck)==0:
            break
    return productID

def randomResetToken():
    while True:
        token= get_random_string(20)
        tokenExists = ResetToken.objects.filter(token=token)
        if len(tokenExists)==0:
            break
    return token


class Product(models.Model):
    name=models.CharField(max_length=200)
    image=models.CharField(max_length=200)
    images=ArrayField(models.CharField(max_length=200),blank=True,null=True)
    price=models.FloatField()
    stock=models.IntegerField()
    itemCategory=models.CharField(max_length=100,default='Other')
    itemType=models.CharField(max_length=100,default='Other')
    size=models.CharField(max_length=50,default=0,blank=True,null=True)
    productID=models.CharField(max_length=20,default=randomProductID)
    colors=models.CharField(max_length=50,blank=True,null=True,default='')
    def __str__(self):
        return self.name

class Featured(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    image= models.CharField(max_length=200,null=True)
    def __str__(self):
        return self.product.name





class Coupons(models.Model):
    code = models.CharField(max_length=50,default="")
    discount = models.IntegerField(default=0)
    def __str__(self):
        return self.code


class TempOrder(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    order_id = models.CharField(max_length=200)
    info = models.TextField()
    total = models.FloatField()
    date_added = models.DateTimeField(auto_now_add=True)

class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,blank=True,null=True)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=200)
    total = models.FloatField()
    status= models.CharField(max_length=100)
    def __str__(self):
        return self.transaction_id

class OrderItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,blank=True,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    quantity = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.order.id)

class ShippingInfo(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    address = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=200)
    email = models.CharField(max_length=200,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.address

class ResetToken(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    token = models.CharField(max_length=200,default=randomResetToken)
    date_added = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.token