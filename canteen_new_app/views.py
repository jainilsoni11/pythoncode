from django.shortcuts import render,render_to_response
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.template.context_processors import csrf
from canteen_new_app.models import Carttable
from django.template.response import TemplateResponse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import Product
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string

count=0

def signup(request):
    c={}
    c.update(csrf(request))
    #if request.GET.get('message','') is not None:
    #    return render_to_response('signup.html',c)
    #else:
    return render_to_response('signup.html',c)

def home(request):
    #
    print(request.user.is_authenticated)
    #
    c={}
    c.update(csrf(request))
    return render(request,'home.html',c)

def aboutus(request):
    c={}
    c.update(csrf(request))
    return render(request,'aboutus.html',c)

def login(request):
    c={}
    c.update(csrf(request))
    #if request.GET.get('msg','') is not None:
    #    return render_to_response('login.html',c)
    #else:
    return render_to_response('login.html',c)

def auth_view(request):
    
    username=request.POST.get('username','')
    password=request.POST.get('password','')
    user=auth.authenticate(username=username,password=password)

    if user is not None:
        auth.login(request,user)
        #
        ob=User.objects.filter(username=username)    # retriving id of user from User table#
        print(ob)
        for j in ob:
            request.session['userid'] = j.id                           # starting session with storing userid in session object #
            #var=j.id
            #print(var)
        #
        return HttpResponseRedirect('/canteen_new_app/loggedin/')
    else:
        return HttpResponseRedirect('/canteen_new_app/login/?msg=Invalid_username_or_password')

def loggedin(request):
    return HttpResponseRedirect('/canteen_new_app/product_info/')

def invalidlogin(request):
    return render_to_response('invalidlogin.html')

def logout(request):
    #auth.logout(request)
    global count
    count=0
    uid=request.session.get('userid')
    request.session.flush()                         #destroy the session
    Carttable.objects.filter(user_id=uid).delete()
    return HttpResponseRedirect('/canteen_new_app/home/')

def addstudentinfo(request):
    uname =request.POST.get('username','')
    passwd = request.POST.get('password','')
    cpasswd = request.POST.get('cpassword','')
    email =request.POST.get('emailid','')
    if User.objects.filter(username=uname).exists()==True:
        return HttpResponseRedirect('/canteen_new_app/signup/?message=Username_already_exist')
    else:
        if(passwd==cpasswd):
            s = User(username=uname,password=make_password(passwd),email=email)
            s.save()
            return HttpResponseRedirect('/canteen_new_app/login/')
        else:
            return HttpResponseRedirect('/canteen_new_app/signup/?message=Password_did_not_match')
# change remaining #
def product_info(request):
    product_item=Product.objects.filter(category='pizza')
    #
    context={'count':count,'product_item':product_item}
    #
    return render(request,'pizza.html',context)

def sandwich(request):
    product_item=Product.objects.filter(category='sandwich')
    context={'count':count,'product_item':product_item}
    return render(request,'pizza.html',context)

def chinese(request):
    product_item=Product.objects.filter(category='chinese')
    context={'count':count,'product_item':product_item}
    return render(request,'pizza.html',context)

def cart(request):
    #
    if request.session.get('userid') is not None:
        uid=request.session.get('userid')               # retrieving user id #
        item=request.POST.get('product_name')           #from hidden field
        category_item=request.POST.get('category')      #from hidden field
        qty=request.POST.get('quantity')
        pr=Product.objects.filter(product_name=item)
        for i in pr:
            p = i.price
        if Carttable.objects.filter(user_id=uid,product_name=item).exists()==True:
            item_get=Carttable.objects.filter(user_id=uid,product_name=item)
            for j in item_get:
                j.quantity=(j.quantity)+int(qty)
                j.save()
        else:        
            s = Carttable(user_id=uid,product_name=item,quantity=qty,price=p)   # storing userid in cart-table to identify perticular user #
            s.save()
            global count
            count+=1
        if(category_item=='pizza'):
            return HttpResponseRedirect('/canteen_new_app/product_info/')
        elif(category_item=='sandwich'):
            return HttpResponseRedirect('/canteen_new_app/sandwich/')
        elif(category_item=='chinese'):
            return HttpResponseRedirect('/canteen_new_app/chinese/')
    else:
        return HttpResponseRedirect('/canteen_new_app/login/')
    #
    
def cart_display(request):
    uid=request.session.get('userid')                   
    data=Carttable.objects.filter(user_id=uid)         # to identify perticular user's cart #
    total=0
    for i in data:
        total=total+((i.quantity)*(i.price))
    context={'data':data,'total':total}
    print(total)
    return render(request,'cart.html',context)

def remove(request):
    global count
    count=count-1
    uid=request.session.get('userid')
    productName=request.POST.get('product_name')        #from hidden field
    Carttable.objects.filter(user_id=uid,product_name=productName).delete()
    return HttpResponseRedirect('/canteen_new_app/cart_display/')    

def bill(request):
    uid=request.session.get('userid')
    if uid is not None:
        o_items=Carttable.objects.filter(user_id=uid)
        if Carttable.objects.filter(user_id=uid).exists()==True:
            #name=User.objects.filter(id=uid)
            total_amount=request.POST.get('amount')     # from hidden field
            #
            for i in o_items:                           # updating product table as the order placed by decreasing quantity #
                pname=i.product_name
                quantity=i.quantity
                p=Product.objects.get(product_name=pname)
                p.quantity=p.quantity-quantity
                #
                if(p.quantity<0):                       # out of stock msg
                    data=Carttable.objects.filter(user_id=uid)
                    msg='out of stock'
                    total=0
                    for i in data:
                        total=total+((i.quantity)*(i.price))
                    context={'data':data,'msg':msg,'total':total}
                    return render(request,'cart.html',context)
                #
                p.save()
            #
            #for i in name:
            #    cust_name=i.username
            order_id=get_random_string(length=5)
            context={'orderId':order_id,'order_items':o_items,'total':total_amount}
            return render(request,'bill.html',context)
        else:
            return HttpResponseRedirect('/canteen_new_app/cart_display/')
    else:
        return HttpResponseRedirect('/canteen_new_app/login/')
# Create your views here.

