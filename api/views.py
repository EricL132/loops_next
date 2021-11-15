
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import *
from django.db.models import Q
from .paypal import create_order,capture_order
import json

import smtplib
import os
from dotenv import load_dotenv

from . import semail 
load_dotenv()
class GetProducts(APIView):
    def get(self,request,format=None):
        products = Product.objects
        return Response({'products':list(products.values())},status=status.HTTP_200_OK)

class GetMensProducts(APIView):
    def get(self,request,format=None):
        products = Product.objects.filter(itemCategory='mens',itemType=request.GET.get('type'),stock__gt=0).values()
        return Response({'products':list(products)},status=status.HTTP_200_OK)

class GetWomensProducts(APIView):
    def get(self,request,format=None):
        products = Product.objects.filter(itemCategory='womens',itemType=request.GET.get('type'),stock__gt=0).values()        
        return Response({'products':list(products)},status=status.HTTP_200_OK)
class GetKidsProducts(APIView):
    def get(self,request,format=None):
        products = Product.objects.filter(itemCategory='kids',itemType=request.GET.get('type'),stock__gt=0).values()        
        return Response({'products':list(products)},status=status.HTTP_200_OK)


class GetProduct(APIView):
    def get(self,request,format=None):
        product = Product.objects.filter(productID=request.GET.get('productid'))
        val = list(product.values())
        for i in val:
            if i.get('images')!=None:
                newlist = ','.join(i.get('images')).split('https')
                newlist.remove('')
                for j in range(len(newlist)):
                    if newlist[j][len(newlist[j])-1] == ',':
                        newlist[j] = newlist[j][0 : len(newlist[j])-1]
                    newlist[j] = 'https'+newlist[j]
                i['images'] = newlist
        return Response(val)

class PopulateOldWithProductID(APIView):
    productExistCheck = Product.objects.filter()
    for k in productExistCheck:
        if k.productID == None:
            k.productID = randomProductID()
            k.save()
    

class GetFeatured(APIView):
    def get(self,request,format=None):
        feature = Featured.objects.all()
        feature = list(feature.values())
        for k in feature:
            k['pid'] = Product.objects.filter(id=k.get('product_id')).values('productID')[0].get('productID')
        return Response(list(feature),status=status.HTTP_200_OK)


class Register(APIView):
    def post(self,request,format=None):
        for i in request.data:
            if not request.data[i]:
                return Response('Please fill out all info',status=status.HTTP_403_FORBIDDEN)
        if not '@' in request.data['email'] or not '.' in request.data['email']:
            return Response('Invalid Email',status=status.HTTP_403_FORBIDDEN)
        if len(request.data['password'])<6:
            return Response('Password must be at least 6 characters',status=status.HTTP_403_FORBIDDEN)
        if len(User.objects.filter(username=request.data['email']))>0:
            return Response('Email already registered',status=status.HTTP_403_FORBIDDEN)
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
            
        email = request.data['email'].lower()
        user = User.objects.create_user(username=email,email=email,password=request.data['password'],first_name=request.data['fname'],last_name=request.data['lname'])
        token = Token.objects.create(user=user)
        token.id = user.id
        token.save()
        self.request.session['auth'] = token.key
        return Response('Registered',status=status.HTTP_200_OK)
class Login(APIView):
    def post(self,request,format=None):
        email = request.data["email"].lower()
        user = authenticate(username=email,password=request.data["password"])
        if user:
            if not self.request.session.exists(self.request.session.session_key):
                self.request.session.create()
            token = Token.objects.filter(user=user)
            if token:
                token.delete()
            token = Token.objects.create(user=user)
            token.id = user.id
            token.save()
            self.request.session["auth"]=token.key
            return Response({},status=status.HTTP_200_OK)
        return Response('Invalid Email/Password',status=status.HTTP_403_FORBIDDEN)

class Forgot(APIView):
    def post(self,request,format=None):
        if request.data["email"]==None:
            return Response('Invalid Information',status=status.HTTP_403_FORBIDDEN)
        email = request.data["email"].lower()
        user = User.objects.filter(email=email)
        if len(user)==0:
            return Response('Email not registered',status=status.HTTP_403_FORBIDDEN)
        user = user[0]
        token = ResetToken.objects.filter(user=user)
        if len(token)>0:
            token = token[0].token
        else:
            token = ResetToken.objects.create(user=user)
            token=token.token
        # with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
        #     smtp.login(os.getenv("EMAIL_ADDRESS"),os.getenv("EMAIL_PASSWORD"))
        #     subject = "Forgot Password"
        #     body= "Reset Link: {}{}".format(os.getenv("HOSTLINK"),token)
        #     msg = f'Subject:{subject}\n\n{body}'
        #     smtp.sendmail(os.getenv("EMAIL_ADDRESS"),user.email,msg)
        semail.main("Forgot password","Reset Link: {}{}".format(os.getenv("WEBLINK"),token),"moomeowmoo1@gmail.com",user.email)
        return Response('Email Sent',status=status.HTTP_200_OK)
            
class Reset(APIView):
    def post(self,request,token,format=None):
        if len(request.data['password'])<6:
            return Response('Password must be at least 6 characters',status=status.HTTP_403_FORBIDDEN)
        if request.data['password']!= request.data['cpassword']:
            return Response('Password and Confirm password must be the same',status=status.HTTP_403_FORBIDDEN)
        token = ResetToken.objects.filter(token=token)
        if len(token)==0:
            return Response('Invalid Token',status=status.HTTP_403_FORBIDDEN)
        token = token[0]
        user = token.user
        user.set_password(request.data['password'])
        user.save()
        token.delete()
        return Response('Password Changed',status=status.HTTP_200_OK)      

class GetAccountInfo(APIView):
    def get(self,request,format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        if 'auth' not in request.session:
            return Response({},status=status.HTTP_403_FORBIDDEN)
        if checkAuth(self.request.session["auth"]):
            return Response({},status=status.HTTP_200_OK)        
        return Response({},status=status.HTTP_403_FORBIDDEN)

class LogOut(APIView):
    def post(self,request,format=None):
        token = Token.objects.filter(key=self.request.session["auth"])
        if token:
            token.delete()
            return Response({},status=status.HTTP_200_OK)
        else:
            return Response('Not Logged In',status=status.HTTP_404_NOT_FOUND)
            
class GetInfo(APIView):
    def get(self,request,format=None):
        token = Token.objects.filter(key=self.request.session["auth"])
        if token:
            user = User.objects.filter(id=token[0].user_id)[0]
            customer = Customer.objects.filter(user=user)
            if customer:
                order = Order.objects.filter(customer=customer[0]).values()
                if order:
                    return Response({"first_name":user.first_name,"last_name":user.last_name,"order":order},status=status.HTTP_200_OK)
            return Response({"first_name":user.first_name,"last_name":user.last_name},status=status.HTTP_200_OK)
        else:
            return Response({},status=status.HTTP_401_UNAUTHORIZED)


class SearchItem(APIView):
    def get(self,request,format=None):
        searchParam = request.GET.get('search',None)
        products = Product.objects.filter(Q(name__icontains=searchParam)).values()
        if products:
            return Response({'products':list(products)},status=status.HTTP_200_OK)
        return Response({'products':[]},status=status.HTTP_200_OK)


class CheckCoupon(APIView):
    def get(self,request,format=None):
        code = Coupons.objects.filter(code=request.GET.get('code',None)).values("discount")
        if len(code)>0:
            return Response(list(code)[0],status=status.HTTP_200_OK)
        else:
            return Response('Invalid Discount Code',status=status.HTTP_404_NOT_FOUND)



class CheckStock(APIView):
    def post(self,request,format=None):
        stock = checkStock(request)
        return Response(stock,status=status.HTTP_200_OK)




class CreateOrder(APIView):
    def post(self,request,format=None):
        total = 0
        stock = checkStock(request.data["cart"])
        if stock.get("status")==False:
            return Response(stock,status=status.HTTP_200_OK)
        if "coupon" in request.data:
            total = round(calculateTotal(request.data["cart"],request.data["coupon"]),2)
        else:
            total = round(calculateTotal(request.data["cart"],False),2)
        order = create_order(total)
        if self.request.session and 'auth' in self.request.session:
            token = Token.objects.filter(key = self.request.session["auth"]).values()
            if token:
                user = User.objects.filter(id=token[0].get("user_id"))[0]
                TempOrder.objects.create(user=user,order_id=order.id,info=json.dumps(request.data),total=total)
            else:
                TempOrder.objects.create(order_id=order.id,info=json.dumps(request.data),total=total)
        else:
            TempOrder.objects.create(order_id=order.id,info=json.dumps(request.data),total=total)
        return Response({"id":order.id},status=status.HTTP_200_OK)

class CaptureOrder(APIView):
    def post(self,request,order,format=None):
        response = capture_order(order)
        if response.result.status=="COMPLETED":
            order_info = TempOrder.objects.filter(order_id=order).values()[0]
            if order_info:
                user = None
                user_info = None
                customer = None
                order_model=None
                info = json.loads(order_info.get("info"))
                if order_info.get("user_id"):
                    user = User.objects.filter(id=order_info.get("user_id"))[0]
                    user_info = User.objects.filter(id=order_info.get("user_id")).values("id","first_name","last_name","email")[0]
                    customer = Customer.objects.filter(user=user)
                    if len(customer)==0:
                        customer = Customer.objects.create(user=user,name=str(user_info.get("first_name"))+" "+str(user_info.get("last_name")),email=user_info.get("email"))
                    else:
                        customer = customer[0]
                else:
                    customer = Customer.objects.create(name=info.get("first_name")+" "+info.get("last_name"),email=info.get("email"))
                order_model = Order.objects.filter(transaction_id=order_info.get("order_id"))
                if len(order_model)==0:
                    order_model = Order.objects.create(customer=customer,transaction_id=order_info.get("order_id"),total=order_info.get("total"),status="Complete")
                else:
                    order_model = order_model[0]
                for i in info.get("cart"):
                    product = Product.objects.filter(id=info.get("cart")[i].get("id"))[0]
                    product.stock = product.stock-info.get("cart")[i].get("quantity")
                    product.save()
                    OrderItem.objects.create(product=product,order=order_model,quantity=info.get("cart")[i].get("quantity"))
                shipping = ShippingInfo.objects.create(customer=customer,order=order_model,address=info.get("address"),state=info.get("state"),city=info.get("city"),zipcode=info.get("zip"),email=info.get("email"))
                return Response({"status":"COMPLETE","order_id":order},status=status.HTTP_200_OK)
            else:
                return Response({"status":"FAIL","error":"Order not found"},status=status.HTTP_403_FORBIDDEN)

class GetOrderInfo(APIView):
    def get(self,request,order):
        order_info = Order.objects.filter(transaction_id=order)[0]
        if order_info:
            shipping_info = ShippingInfo.objects.filter(order=order_info).values()[0]
            products = OrderItem.objects.filter(order=order_info).values("product_id","quantity")
            for i in products:
                product = Product.objects.filter(id=i.get("product_id")).values("image","name","price","size","productID")[0]
                i["product_id"] = product
            return Response({"shipping_info":shipping_info,"order_info":products,"total":order_info.total},status=status.HTTP_200_OK)
        else:
            return Response({},status=status.HTTP_404_NOT_FOUND)
def checkAuth(token):
    token = Token.objects.filter(key=token)
    if token:
        return True
    return False

def checkStock(data):
    allInStock = True
    for i in data:
        product = Product.objects.filter(id=data[i].get("id")).values()
        if data[i].get("quantity")==0 or data[i].get("quantity") >product[0].get("stock"):
            data[i]["quantity"] = 0
            allInStock = False
    if allInStock==False:
        return {"status":allInStock,"cart":data}
    else:
        return {"status":allInStock}
def calculateTotal(cart,coupon):
    discount = False
    total = 0
    if coupon:
        code = Coupons.objects.filter(code=coupon.strip()).values("discount")
        if len(code)>0:
            discount = code[0].get("discount")
   
    for i in cart:
        total += cart[i].get("price")*cart[i].get("quantity")
    if discount:
        total = total - total*(discount/100)
    total = total + (total*.08)
    return total