from django.shortcuts import get_object_or_404, render,redirect
from .forms import CustomerCreationForm, SellerCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from product.models import Product,Category,Cart,ShippingAddress,Order,OrderItem
from django.db.models import Q
import datetime
from .models import Customer, CustomUser


# Create your views here.
def customer_signup(request):
    if request.method == 'POST':
        form = CustomerCreationForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('signin')
        else:
            
            return render(request, "customer_signup.html",{"form": form})
    else:
        form = CustomerCreationForm()
    return render(request, "customer_signup.html",{"form": form})


def seller_signup(request):
    if request.method == 'POST':
        form = SellerCreationForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            error = "Something went wrong"
            return render(request, "seller_signup.html",{"error": error},{"form": form})
    else:
        form = SellerCreationForm()
    return render(request, "seller_signup.html",{"form": form})



def signin(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
        else:
            
            return render(request,"signin.html",{"form":form})
           
    else:
        form = AuthenticationForm()
    return render(request,"signin.html",{'form':form})

def signout(request):
    logout(request)
    return redirect("index")

def index(request):
    products = Product.objects.all()
    context ={
        'products':products
    }
    return render(request,"index.html",context)



def category(request):
    category = request.GET.get('product')
    cat_object = Category.objects.get(name=category)
    products = Product.objects.filter(category=cat_object)
    context={
        'products':products
    }
    return render(request,"index.html",context)


def search_bar(request):
    value = request.GET['search_bar']
    products = Product.objects.none()
    if value is not None:
        category_query = Product.objects.filter(category__name__icontains=value)
        title_query = Product.objects.filter(title__icontains=value)
        description_query = Product.objects.filter(description__icontains=value)

    products = category_query | title_query | description_query    
    context ={
        'products':products
    }
    return render(request,"index.html",context)

def sorting(request):
    value = request.GET.get('sort')
    if value == 'lth':
        products = Product.objects.order_by('price')
    else:
        products = Product.objects.order_by('-price')

    context ={
        'products':products
    }
    return render(request,"index.html",context) 


def product_details(request,id):
    product=Product.objects.get(id=id)
    date=datetime.datetime.today().date()+datetime.timedelta(days=5)
    context ={
        'product':product,
        'date':date
    }
    return render(request,"product_details.html",context)


def add_to_cart(request,id):
    product=Product.objects.get(id=id)
    if request.user.is_authenticated:
        try:
            customer=Customer.objects.get(id=request.user.id)
        except Customer.DoesNotExist:
            return redirect('signin')    
    else:
        return redirect('signin')
           
   
    cart_item,created=Cart.objects.get_or_create(product=product,customer=customer)
    if not created:
        cart_item.quantity +=1

    else:
        cart_item.quantity =1

    cart_item.save()
    return redirect('cart')       
    

def cart(request):
    if request.user.is_authenticated:
        try:
            customer=Customer.objects.get(id=request.user.id)
        except Customer.DoesNotExist:
            return redirect('signin') 
        items=Cart.objects.filter(customer=customer)   
        
        total_amount=0
        for item in items:
            total_amount += item.product.price * item.quantity
        context={
            'items': items,
            'total_amount':total_amount,
            'total_items':len(items),
        }    

        return render(request,'cart.html',context)
    else:
        return redirect('signin')
    
        
def updateqty(request,id):
    product = Cart.objects.get(product=id,customer=request.user)
    val=request.GET.get('var')
    if val == "0":
        if product.quantity>1:
            product.quantity-=1
    else: 
        product.quantity+=1
    product.save()
    return redirect('cart')    

def remove_item(request,id):
    product = Cart.objects.get(product=id,customer=request.user)
    product.delete()
    return redirect('cart')


def address(request):
    if request.method == 'POST':
        address_line = request.POST['address']
        landmark = request.POST['landmark']
        city = request.POST['city']
        state = request.POST['state']
        pincode = request.POST['pincode']
        user = Customer.objects.get(id=request.user.id)
        total_address = ShippingAddress.objects.filter(customer=user)
        if len(total_address) < 3:
            address = ShippingAddress.objects.create(customer=user, address_line1=address_line,landmark=landmark,city=city,state=state,pincode=pincode)
            address.save()
            return redirect('address')
        else:
            return redirect('address')


    else:
        addresses = ShippingAddress.objects.filter(customer=request.user)
        context ={
            'addresses':addresses
        }
    return render(request,'address.html',context)



def update_address(request,id):
    update_address = ShippingAddress.objects.get(id=id)
    addresses = ShippingAddress.objects.filter(customer=request.user)
    if request.method == 'POST':
        update_address.address_line1 = request.POST['address']
        update_address.landmark = request.POST['landmark']
        update_address.city = request.POST['city']
        update_address.state = request.POST['state']
        update_address.pincode = request.POST['pincode']
        update_address.save()
        return redirect('address')
        
    context ={
        'addresses':addresses,
        'update_address':update_address
        }
    return render(request,'address.html',context)
        

def delete_address(request,id):
    address = ShippingAddress.objects.get(id=id)
    address.delete()
    return redirect('address')



def confirm_order(request,id):
    if request.user.is_authenticated:
        cart_item = Cart.objects.filter(customer=request.user)
        address = ShippingAddress.objects.get(id=id)
        total_amount=0
        for item in cart_item:
            total_amount += item.product.price * item.quantity
        context={
            'cart_items':cart_item,
            'address':address,
            'total_amount':total_amount
        }
        return render(request,'confirm_order.html',context)
    else:
        return redirect('signin') 
       
import random
import razorpay
def payment(request,id):
     if request.user.is_authenticated:
        cart_item = Cart.objects.filter(customer=request.user)
        address = ShippingAddress.objects.get(id=id)
        total_amount=0
        for item in cart_item:
            total_amount += item.product.price * item.quantity
        order_id=random.randrange(1000,9999)  
        customer=Customer.objects.get(id=request.user.id)
        date=datetime.datetime.today().date()
        order=Order.objects.create(order_id=order_id,customer=customer,order_date=date,shipping_address=address,order_amount=total_amount)  
        order.save()
        for item in cart_item:                                                                         
            OrderItem.objects.create(order=order,product=item.product,quantity=item.quantity,unit_price=item.product.price) 
        cart_item.delete() 
        client = razorpay.Client(auth=("rzp_test_n0lhpmrEfeIhGJ","UOrbXQGnsEc2dhB1IFg0zNWZ")) 
        data={"amount":int(total_amount*100),"currency":"INR","receipt":str(order_id)}
        payment=client.order.create(data=data)   

     context={
        'data':data,
        'payment':payment,
        
     }
     return render(request,'pay.html',context)

def payment_success(request):
    payment_id = request.GET.get('payment_id', 'N/A')
    order_id = request.GET.get('order_id', 'N/A')

    order = get_object_or_404(Order, order_id=order_id)

    order.payment_status = 'paid'
    order.save()

    return render(request, 'payment_success.html', {
        'payment_id': payment_id,
        'order_id': order_id
    })



def my_orders(request):
    if request.user.is_authenticated:
        orders=Order.objects.filter(customer=request.user)
        context={'orders': orders}
        return render(request, 'my_orders.html',context)
    else:
        return redirect('signin')

from .forms import PasswordResetForm
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.core.mail import send_mail
from django.conf import settings

def generate_otp(user):
    otp = str(random.randint(100000,999999))
    return otp

def forgot_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = CustomUser.objects.get(email=email)
                otp = generate_otp(user)
                request.session['otp'] = otp
                request.session['request_user'] = user.id

                send_mail(
                    'password Reset OTP', #email subject
                    f'Your OTP For Password Reset Is : {otp}', #message
                    settings.EMAIL_HOST_USER, #sender mail
                    [user.email], #reciever mail
                    fail_silently=False,

                )
                return redirect('verify_otp')


            except CustomUser.DoesNotExist:
                messages.error(request,"No user found with this email")
                return render(request,'password_reset_request.html',{'form':form})
                
            


    else:
        form = PasswordResetForm()
        context = {'form': form}
    return render(request,'password_reset_request.html',{'form':form})


def verify_otp(request):
    if request.method=='POST':
        otp_entered = request.POST['otp']
        otp_stored = request.session['otp']

        if otp_entered == otp_stored:
            user_id = request.session['request_user']
            if user_id:
                user = CustomUser.objects.get(id=user_id)
                return redirect('reset_password',user_id=user.id)
            else:
                messages.error(request,"Session expired, please request OTP again.")
                return redirect('forgot_password')
        else:
            messages.error(request,"Invalid or expired OTP")
            return render(request,'verify_otp.html')



    return render(request,'verify_otp.html')
    
    
def reset_password(request,uder_id):
    pass

    
