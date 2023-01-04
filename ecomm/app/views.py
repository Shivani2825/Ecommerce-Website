from itertools import product
from statistics import quantiles
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User





# def buy_now(request):
#  return render(request, 'app/buynow.html')

def profile(request):
 return render(request, 'app/profile.html')

def address(request):
 return render(request, 'app/address.html')

def orders(request):
 return render(request, 'app/orders.html')

def change_password(request):
 return render(request, 'app/changepassword.html')

def mobile(request):
 return render(request, 'app/mobile.html')

def login(request):
 return render(request, 'app/login.html')

def customerregistration(request):
 return render(request, 'app/customerregistration.html')

def checkout(request):
 return render(request, 'app/checkout.html')

class ProductView(View):
    def get(self, request):
        topwears = Product.objects.filter(category='TW')
        bottomwears= Product.objects.filter(category='BW')
        mobiles= Product.objects.filter(category='M')
        laptops= Product.objects.filter(category='L')
        return render(request, 'app/home.html',
        {'topwears':topwears, 'bottomwears':bottomwears, 'mobiles': mobiles,"laptops":laptops})


class ProductDetailView(View):
    def get(self,request,pk):
        product=Product.objects.get(pk=pk)
        item_already_in_cart=False
        if request.user.is_authenticated:
            item_already_in_cart=Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
            return render(request, 'app/productdetail.html',{'product':product, 'item_already_in_cart':item_already_in_cart})
        else:
            return render(request, 'app/productdetail.html',{'product':product, 'item_already_in_cart':item_already_in_cart})

# @login_required
class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
            return render(request, 'app/productdetail.html',{'product':product, 'item_already_in_cart':item_already_in_cart})
        else:
            return render(request, 'app/productdetail.html',{'product':product, 'item_already_in_cart':item_already_in_cart})
        
# @login_required
def add_to_cart(request):
    user = request.user
    product_id =request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')
     


# @login_required
def show_cart(request):
    try:
        if request.user.is_authenticated:
            user=request.user
            cart= Cart.objects.filter(user=user)
            amount = 0.0
            shipping_amount=70.0
            total_amount=0.0
            cart_product=[p for p in Cart.objects.all() if p.user == user]
            if cart_product:
                for p in cart_product:
                    tempamount=(p.quantity*p.product.discounted_price)
                    amount+= tempamount
                    total_amount=amount+shipping_amount
                return render(request, 'app/addtocart.html',{'carts':cart, 'total_amount':total_amount, 'amount':amount})
    except:
                return render(request, 'app/emptycart.html')



@login_required
def plus_cart(request):
    if request.method == 'GET':
        prod_id= request.GET['cart_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount =0.0
        shipping_amount=70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount=(p.quantity * p.product.discounted_price)
            amount+= tempamount
            

        data ={
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount + shipping_amount
            }
        return JsonResponse(data)

@login_required
def minus_cart(request):
    if request.method == 'GET':
        prod_id= request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount =0.0
        shipping_amount=70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount=(p.quantity * p.product.discounted_price)
            amount-= tempamount
            

        data ={
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': amount + shipping_amount
            }
        return JsonResponse(data)

@login_required
def remove_cart(request):
    if request.method == 'GET':
        prod_id= request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount =0.0
        shipping_amount=70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount=(p.quantity * p.product.discounted_price)
            amount+= tempamount

        data ={
             'amount': amount,
            'totalamount': amount + shipping_amount
            }
        return JsonResponse(data)


@login_required
def buy_now(request):
    return render(request, 'app/buynow.html')

@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount=0.0
    shipping_amount=70.0
    totalamount= 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            tempamount=(p.quantity * p.product.discounted_price)
            amount+= tempamount
        totalamount= amount+ shipping_amount
    return render(request, 'app/checkout.html',{'add': add, 'totalamount':totalamount, 'cart_items':cart_items})

