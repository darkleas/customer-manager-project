from django.shortcuts import render,get_object_or_404,redirect,HttpResponseRedirect
from django.http import HttpResponse
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
import datetime
from PIL import Image
from django.core.files import File
from io import BytesIO
import sys
import os
from django.core.files.uploadhandler import InMemoryUploadedFile
# Create your views here.

def home(request):
    # Last 5 Day Orders Graphic
    x = datetime.datetime.now()
    days = datetime.timedelta(1)
    newdate = x - days
    days = datetime.timedelta(2)
    newdate1 = x - days
    days = datetime.timedelta(3)
    newdate2 = x - days
    days = datetime.timedelta(4)
    newdate3 = x - days
    today = datetime.date.today()
    today_orders = Order.objects.filter(date_created__day=x.day).count()
    today_orders1 = Order.objects.filter(date_created__day=newdate.day).count()
    today_orders2 = Order.objects.filter(date_created__day=newdate1.day).count()
    today_orders3 = Order.objects.filter(date_created__day=newdate2.day).count()
    today_orders4 = Order.objects.filter(date_created__day=newdate3.day).count()
    
    today_money = Order.objects.filter(date_created__day=x.day)
    today_money1 = Order.objects.filter(date_created__day=newdate.day)
    today_money2 = Order.objects.filter(date_created__day=newdate1.day)
    today_money3 = Order.objects.filter(date_created__day=newdate2.day)
    today_money4 = Order.objects.filter(date_created__day=newdate3.day)

    a1 = 0
    b2 = 0
    c3 = 0
    d4 = 0
    e5 = 0
    for a in today_money:
        a1 += a.product.price
    for b in today_money1:
        b2 += b.product.price
    for c in today_money2:
        c3 += c.product.price
    for d in today_money3:
        d4 += d.product.price
    for e in today_money4:
        e5 += e.product.price







    labels = ['{0}'.format(newdate3.strftime("%A")),'{0}'.format(newdate2.strftime("%A")),'{0}'.format(newdate1.strftime("%A")),'{0}'.format(newdate.strftime("%A")),'Today']
    data = [today_orders4,today_orders3,today_orders2,today_orders1,today_orders]

    labels2 = ['{0}'.format(newdate3.strftime("%A")),'{0}'.format(newdate2.strftime("%A")),'{0}'.format(newdate1.strftime("%A")),'{0}'.format(newdate.strftime("%A")),'Today']
    data2 = [str(e5),str(d4),str(c3),str(b2),str(a1)]

    # Customers table
    customers = Customer.objects.filter().order_by('-id')

    # Total Orders
    orders = Order.objects.all()
    total_orders = orders.all().count()
    order_delivered = orders.filter(status='Delivered').count()
    order_pending = orders.filter(status='Pending').count()
    z = Order.objects.filter(date_created__day=x.day)
    total = 0
    for i in z:
        total += int(i.product.price)
    
    new_users = Customer.objects.all().order_by('-id')[:8]
    
    context = {'new_users':new_users,'total_money':(str(total)+' $'),'labels':labels,'data':data,'labels2':labels2,'data2':data2,'customers':customers,
    'total_orders':total_orders,'order_delivered':order_delivered,'order_pending':order_pending}
    return render(request,'accounts/dashboard.html',context)
@login_required(login_url='/login/')
def products(request):
    products = Product.objects.all()
    context={'products':products,'circle':'isntnull'}
    return render(request,'accounts/products.html',context)
@login_required(login_url='/login/')
def orders(request):
    orders = Order.objects.all()
    context={'orders':orders}
    return render(request,'accounts/orders.html',context)
@login_required(login_url='/login/')
def customer(request,pv):
    customer = get_object_or_404(Customer,id=pv)
    orders = customer.order_set.all()
    order_count = orders.count()
    context = {'customer':customer,'orders':orders,'order_count':order_count}
    return render(request,'accounts/customer.html',context)
@login_required(login_url='/login/')
def order_create(request):
    form = OrderForm()
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            frm = form.save(commit=False)
            frm.customer = request.user.customer
            frm.status = "Pending"
            frm.save()
            messages.success(request, "Order created successfully")
            return redirect('/orders/')

    context = {'form':form}
    return render(request,'accounts/order_form.html',context) 
@login_required(login_url='/login/')
def order_update(request,pv):
    order = Order.objects.get(id=pv)
    form = OrderUpdateForm(instance=order)
    if request.method == "POST":
        form = OrderUpdateForm(request.POST,instance=order)
        if form.is_valid():
            if request.user.is_superuser:
                form.save()
                messages.warning(request, "Order updated successfully")
                return redirect('/orders/')
            messages.info(request, "You don't have permission to update order")
            context = {'form':form}
            return render(request,'accounts/order_form.html',context) 

    context = {'form':form}
    return render(request,'accounts/order_form.html',context) 
@login_required(login_url='/login/')
def delete_order(request,pv):
    order = Order.objects.get(id=pv)
    if request.method == "POST":
        if request.user.is_superuser:
            order.delete()
            messages.success(request, "Order deleted successfully")
            return redirect('/orders/')
        messages.info(request, "You don't have permission to delete order")
        context = {'order':order}
        return render(request,'accounts/order_delete.html',context) 

    context = {'order':order}
    return render(request,'accounts/order_delete.html',context) 

def Login(request):
    if request.user.is_authenticated:
        return redirect("/")

    else:
        next = ""
        if request.GET:
            next = request.GET['next']
        if request.method == "POST":

            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request,username=username,password=password)
            if user is None:
                return render(request,'accounts/login.html',{"error":"Username or password is wrong. Please try again",'next':next}) 
            else:
                messages.success(request, username + " logined successfully")
                login(request,user)
                if next == "":
                    return redirect("/")
                else:
                    return redirect(next)


        return render(request,'accounts/login.html',{'next':next}) 
    
def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            Customer.objects.create(
                user=user,
                name=user.username,
                
            )
            messages.success(request, "User created successfully")
            return redirect('/')
    context = {'form':form}
    return render(request,'accounts/register.html',context) 
def Logout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "User exit successfully")
        return redirect("/login/")
    else:
        messages.warning(request, "You are not logged in. You should login to logout")
        return redirect("/login/")
def userPage(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.all().count()
    order_delivered = orders.filter(status='Delivered').count()
    order_pending = orders.filter(status='Pending').count()
    context = {'orders':orders,'total_orders':total_orders,'order_delivered':order_delivered,'order_pending':order_pending}
    return render(request,'accounts/userpage.html',context) 
@login_required(login_url='/login/')

def accountPage(request):
    form = CustomerForm(instance=request.user.customer)
    form2 = PasswordChangeForm(request.user)
    form3 = ProfilePictureForm(instance=request.user.customer)

    if request.method == "POST":
        if "name" in request.POST:
            form = CustomerForm(request.POST,request.FILES,instance=request.user.customer)
            if form.is_valid():
                password = request.POST['password']
                user = authenticate(username=request.user.username, password=password)

                if user is not None:
                    form.save()
                    userz = User.objects.get(username=request.user.username,password=request.user.password)
                    if request.POST['email'] == "":
                        userz.email = "."

                    else:
                        userz.email = form.cleaned_data.get('email')
                    userz.save()    
                    messages.success(request, "Update is successful")
                    return redirect("/account/")
                else:
                    messages.info(request, "Confirm password is wrong")
                    return redirect("/account/")
        elif "new_password1" in request.POST:
            form2 = PasswordChangeForm(request.user,request.POST)
            if form2.is_valid():
                form2.save()
                logout(request)
                messages.success(request, "Password successfully changed")

                return redirect("/login/")
        elif "removepicture" in request.POST:
            Customer.objects.get(user=request.user).profile_pic.delete(save=True)
            #user = Customer.objects.get(user=request.user)
            #user.profile_pic = None
            #user.save()
            messages.info(request, "Profile picture successfully removed")

            return redirect("/account/")

        elif "name" not in request.POST and "new_password1" not in request.POST:
            form3 = ProfilePictureForm(request.POST,request.FILES,instance=request.user.customer)
            if form3.is_valid():
                Customer.objects.get(user=request.user).profile_pic.delete(save=True)

                fto = form3.save(commit=False)

                uploadedImage = form3.cleaned_data.get('profile_pic')

                imageTemproary = Image.open(uploadedImage)
                outputIoStream = BytesIO()
                imageTemproary = imageTemproary.resize( (800,800) ) 
                imageTemproary = imageTemproary.convert('RGB')
                imageTemproary.save(outputIoStream , format='JPEG', quality=70)
                outputIoStream.seek(0)
                uploadedImage = InMemoryUploadedFile(outputIoStream,'ImageField', "%s.jpg" % uploadedImage.name.split('.')[0], 'image/jpeg', sys.getsizeof(outputIoStream), None)



              

            
            
                fto.profile_pic = uploadedImage
                fto.save()
                messages.success(request, "Profile picture successfully changed")
                return redirect("/account/")

            return render(request,'accounts/account.html',{'form':form,'form2':form2,'form3':form3}) 



    return render(request,'accounts/account.html',{'form':form,'form2':form2,'form3':form3}) 

def passwordresetsent(request):
    messages.warning(request, "We’ve emailed you instructions for setting your password, if an account exists with the email you entered")

    return redirect("/reset_password/")
def passwordresetcomplete(request):
    messages.success(request, "Your password has been set. You may go ahead and log in now")

    return redirect("/")
@login_required(login_url='/login/')
def product_create(request):
    form = ProductForm()
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Product created successfully")
            return redirect('/products/')

    context = {'form':form}
    return render(request,'accounts/product_form.html',context) 
@login_required(login_url='/login/')

def product_update(request,pv):
    product = Product.objects.get(id=pv)
    form = ProductForm(instance=product)
    if request.method == "POST":
        form = ProductForm(request.POST,instance=product)
        if form.is_valid():
            if request.user.is_superuser:
                form.save()
                messages.success(request, "Product updated successfully")
                return redirect('/products/')
            messages.info(request, "You don't have permission to update product")
            context = {'form':form}
            return render(request,'accounts/product_form.html',context) 

    context = {'form':form}
    return render(request,'accounts/product_form.html',context) 
@login_required(login_url='/login/')
def delete_product(request,pv):
    product = Product.objects.get(id=pv)
    if request.method == "POST":
        if request.user.is_superuser:
            product.delete()
            messages.success(request, "Product deleted successfully")
            return redirect('/products/')
        messages.info(request, "You don't have permission to delete product")
        context = {'product':product}
        return render(request,'accounts/product_delete.html',context) 

        

    context = {'product':product}
    return render(request,'accounts/product_delete.html',context) 
