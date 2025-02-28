from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from .models import *
import os
from django.contrib.auth.decorators import login_required
import razorpay
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponse
from django.http import JsonResponse
import json
from django.conf import settings
from django.db.models import Q
from django.utils.crypto import get_random_string
from django.views.decorators.csrf import csrf_exempt
from .constants import PaymentStatus
# Create your views here.

def m_login(req):
    if 'admin' in req.session:
        return redirect(admin_home)
    if 'user' in req.session:
        return redirect(user_prfl)
    if req.method=='POST':
        uname=req.POST['username']
        password=req.POST['password']
        data=authenticate(username=uname,password=password)
        if data:
            if data.is_superuser:
                login(req,data)
                req.session['admin']=uname
                return redirect(admin_home)
            else:
                login(req,data)
                req.session['user']=uname
                return redirect(user_home)
        else:
            messages.warning(req,"Invalid uname or password")
            return redirect(m_login)
    else:
        return render(req,'login.html')


# def reg(req):
#         if req.method=='POST':
#             name=req.POST['name']
#             email=req.POST['email']
#             password=req.POST['password']
#             try:
#                 send_mail('user registration', 'account created', settings.EMAIL_HOST_USER, [email])
#                 data=User.objects.create_user(first_name=name,email=email,password=password,username=email)
#                 data.save()
#                 return redirect(m_login)
#             except:
#                 messages.warning(req,"Email not valid")
#                 return redirect(reg)
#         else:
#             return render(req,'user/register.html')
        
def reg(req):
        if req.method=='POST':
            name=req.POST['name']
            email=req.POST['email']
            password=req.POST['password']
            if User.objects.filter(email=email).exists():
                messages.warning(req, "Email already registered")
                return redirect(reg)
            otp = get_random_string(length=6, allowed_chars='0123456789')
            req.session['otp'] = otp
            req.session['email'] = email
            req.session['name'] = name
            req.session['password'] = password
            send_mail(
                'Your OTP Code',
                f'Your OTP is: {otp}',
                settings.EMAIL_HOST_USER, [email])
            messages.success(req, "OTP sent to your email")
            return redirect(verify_otp_reg)

    
        return render(req,'user/register.html')

def verify_otp_reg(req):
    if req.method == 'POST':
        entered_otp = req.POST['otp'] 
        stored_otp = req.session.get('otp')
        email = req.session.get('email')
        name = req.session.get('name')
        password = req.session.get('password')
        if entered_otp == stored_otp:
            user = User.objects.create_user(first_name=name,username=email,email=email,password=password)
            user.is_verified = True
            user.save()      
            messages.success(req, "Registration successful! You can now log in.")
            send_mail('User Registration Succesfull', 'Account Created Succesfully And Welcome To Photox', settings.EMAIL_HOST_USER, [email])
            return redirect(m_login)
        else:
            messages.warning(req, "Invalid OTP. Try again.")
            return redirect(verify_otp_reg)

    return render(req, 'verify_otp_reg.html')

def resend_otp_reg(req):
    email = req.session.get('email')
    if email:
        otp = get_random_string(length=6, allowed_chars='0123456789')
        req.session['otp'] = otp
        
        send_mail(
            'Your New OTP Code',
            f'Your OTP is: {otp}',
            settings.EMAIL_HOST_USER, [email]
        )
        messages.success(req, "OTP resent to your email")
    
    return redirect(verify_otp_reg)

def forgetpassword(req):
    if req.method == 'POST':
        email = req.POST['email']
        try:
            user = User.objects.get(email=email)
            otp = get_random_string(length=6, allowed_chars='0123456789')
            req.session['otp'] = otp
            req.session['email'] = email
            send_mail('Password Reset OTP', f'Your OTP is: {otp}', settings.EMAIL_HOST_USER, [email])
            messages.success(req, "OTP sent to your email")
            return redirect(verify_otp)
        except User.DoesNotExist:
            messages.warning(req, "Email not found")
            return redirect(forgetpassword)
    return render(req,'forgetpassword.html')


def verify_otp(req):
    if req.method == 'POST':
        otp = req.POST['otp']
        if otp == req.session.get('otp'):
            return redirect(resetpassword)
        else:
            messages.warning(req, "Invalid OTP")
            return redirect(verify_otp)
    return render(req, 'verify_otp.html')


def resend_otp(req):  
    email = req.session.get('email')
    if email:
        otp = get_random_string(length=6, allowed_chars='0123456789')
        req.session['otp'] = otp
        send_mail('Password Reset OTP', f'Your OTP is: {otp}', settings.EMAIL_HOST_USER, [email])
        messages.success(req, "OTP resent to your email")
    return redirect(verify_otp)


def resetpassword(req):
    if req.method == 'POST':
        password = req.POST['password']  
        email = req.session.get('email')
        try:
            user = User.objects.get(email=email)
            user.set_password(password)
            user.save()
            messages.success(req, "Password reset successfully")
            return redirect(m_login)
        except User.DoesNotExist:
            messages.warning(req, "Error resetting password")
            return redirect(resetpassword)
    return render(req, 'resetpassword.html')
# def admin_home(req):
    
#     data=Category.objects.all()
#     p_data=Plants.objects.all()
    
#     return render(req,'admin/adminhome.html',{'Category':data,'Plants':p_data})
    # return render(req,'admin/adminhome.html',{'Category':data,'Plants':p_data})

def user_home(req):
    data=Plants.objects.all()[::-1]
    c_data=Category.objects.all()
    p_data=Plants.objects.all()
    m_data=Main_cat.objects.all()

    return render(req,'user/userhome.html',{'Plants':data,'c_data':c_data,'p_data':p_data,'m_data':m_data})

def search(req):
    srch = req.GET.get('srch', '').strip()  # Safely get search term
    data = []

    if srch:  # Only search if the term is not empty
        data = Plants.objects.filter(name__icontains=srch)  # Case-insensitive search

    return render(req, 'user/search.html', {'data': data, 'srch': srch})


def homep(req):
    return redirect(user_home)

def a_home(req):
    return redirect(admin_home)

def int_plt(req):
    data=Plants.objects.all()[::-1]
    return render(req,'user/p_1.html',{'Plants':data})

def user_prfl(req):
    # return render(req,'user/userprf.html')
    if 'user' in req.session:
        user=User.objects.get(username=req.session['user'])
        data1=Address.objects.filter(user=user)

        if req.method == 'POST':
            user=User.objects.get(username=req.session['user'])
            name=req.POST['name']
            phn=req.POST['phn']
            pin=req.POST['pin']
            loc=req.POST['loc']
            adrs=req.POST['adrs']
            city=req.POST['city']
            state=req.POST['state']
            data=Address.objects.create(user=user,name=name,phn=phn,pin=pin,loc=loc,adrs=adrs,city=city,state=state)
            data.save()
            return redirect(addrs)
        else:
            return render(req,'user/userprf.html',{'data1':data1})
    else:
        return render(req,"user/userprf.html",{'data1':data1,'user':user})

def user_logout(req):
    req.session.flush()
    logout(req)
    return redirect(user_home)

def admin_logout(req):
    req.session.flush()
    logout(req)
    return redirect(user_home)




def search(req):
    m_data=Main_cat.objects.all()
    c_data=Category.objects.all()
    query = req.GET.get('query', '').strip()  
    if query:
        data = Plants.objects.filter( Q(name__icontains=query))
    else:
        data = [] 
    return render(req, 'user/search.html', {'data': data,'m_data':m_data,'c_data':c_data})

def add_to_cart(req,pid):

    if 'user' in req.session:
        prdct=Plants.objects.get(pk=pid)
        user=User.objects.get(username=req.session['user'])

        try:

            data=Cart.objects.get(user=user,Plants=prdct)
            data.qty+=1
            data.price=data.Plants.offer_price*data.qty
            data.save()
            # return redirect(view_cart)
        except:
            price=prdct.offer_price
            data=Cart.objects.create(user=user,Plants=prdct,qty=1,price=price)
            data.save()
        prdct.stock-=1
        prdct.save()
        return redirect(view_cart)
    else:
        return redirect(m_login)
    

def delete_cart(req,pid):
    if 'user' in req.session:
        data=Cart.objects.get(pk=pid)
        data.delete()
        return redirect(view_cart)
    else:
        return redirect(m_login)


def view_cart(req):
    if 'user' in req.session:
        user=User.objects.get(username=req.session['user'])
        cart_dtls=Cart.objects.filter(user=user)
        m_data=Main_cat.objects.all()
        c_data=Category.objects.all()
        total=0
        for i in cart_dtls:
            total+=i.price
        return render(req,'user/cart.html',{'cart_dtls':cart_dtls,'total':total,'m_data':m_data,'c_data':c_data})
    else:
        return redirect(m_login)

def cartIncrement(req,pid):
    if 'user' in req.session:
        data=Cart.objects.get(pk=pid)
        if data.Plants.stock>0:
            data.qty+=1
            data.price=data.Plants.offer_price*data.qty
            pro=data.Plants
            pro.stock-=1
            pro.save()
            data.save()
        return redirect(view_cart)
    else:
        return redirect(m_login) 
       
def cartDecrement(req,pid):
    if 'user' in req.session:
        data=Cart.objects.get(pk=pid)
        if(data.qty>0):
            data.qty-=1
            data.price=data.Plants.offer_price*data.qty
            pro=data.Plants
            pro.stock+=1
            pro.save()
            data.save()
        if data.qty==0:
            data.delete()
        return redirect(view_cart)
    else:
        return redirect(m_login)



    
def add_Mcatg(req):
    if 'admin' in req.session:
        if req.method=='POST':
            if 'main_form' in req.POST:
                name=req.POST['m_name']
                data=Main_cat.objects.create(m_name=name)
                data.save()
                # return redirect(add_Mcatg)
            elif 'catg_form' in req.POST:
                m_ctg=req.POST['m_ctg']
                name=req.POST['it_ctg']
                # main_cat = Main_cat.objects.get(m_name=m_ctg)
                data2 = Category.objects.create(m_cat=Main_cat.objects.get(m_name=m_ctg), c_name=name)
                data2.save()
            return redirect(add_Mcatg)
        else:
            data=Category.objects.all()
            data1=Main_cat.objects.all()
            return render(req,'admin/add_Mcatg.html',{'Category':data,'Main_cat':data1})
    else:
        return redirect(m_login)

def edit_Mcatg(req,pid):
    data=Main_cat.objects.get(pk=pid)
    if req.method=='POST':
        name=req.POST['m_name']
        data=Main_cat.objects.filter(pk=pid).update(m_name=name)
        return redirect(add_Mcatg)
    else:
        return render(req,'admin/editmcatg.html',{'data':data})

def delete_Mcatg(req,pid):
    data=Main_cat.objects.get(pk=pid)
    data.delete()
    return redirect(add_Mcatg)

def edit_catg(req,pid):
    data=Category.objects.get(pk=pid)
    if req.method=='POST':
        name=req.POST['c_name']
        data=Category.objects.filter(pk=pid).update(c_name=name)
        return redirect(add_Mcatg)
    else:
        return render(req,'admin/editcatg.html',{'data':data})
def delete_catg(req,pid):
    data=Category.objects.get(pk=pid)
    data.delete()
    return redirect(add_Mcatg)


# def buy(req,pid):
#     if 'user' in req.session:
#         user=User.objects.get(username=req.session['user'])
#         prdt=Plants.objects.get(pk=pid)
#         data=Address.objects.filter(user=user)
#         return render(req,'user/buy.html',{'data':data,'prdt':prdt})
#     else:
#         return redirect(m_login)



# Function to view product details
def view_pro(req, pid):
    data = Plants.objects.get(pk=pid)
    m_data = Main_cat.objects.all()
    c_data = Category.objects.all()
    return render(req, 'user/view_pro.html', {'data': data, 'm_data': m_data, 'c_data': c_data})






# Function to buy the product
def buy(req, pid):
    if 'user' in req.session:
        prod = Plants.objects.get(pk=pid)
        user = User.objects.get(username=req.session['user'])
        data = Address.objects.filter(user=user)

        if data:
            # Store product ID in session before proceeding
            req.session['pid'] = prod.pk
            return redirect("orderSummary", prod=prod.pk, data=data)
        else:
            return render(req, "user/adrs.html")
    else:
        return redirect(m_login)

# Order summary page before payment
def orderSummary(req, prod, data):
    if 'user' in req.session:
        prod = Plants.objects.get(pk=prod)
        user = User.objects.get(username=req.session['user'])
        data = Address.objects.filter(user=user)

        if req.method == 'POST':
            address = req.POST['adrs']
            addr = Address.objects.get(user=user, pk=address)
            req.session['address'] = addr.pk  # Store address in session
            return redirect(order_payment)
        else:
            return render(req, 'user/buy.html', {'prod': prod, 'data': data})
    else:
        return redirect('m_login')

# Payment page
def order_payment(req):
    if 'user' in req.session:
        user = User.objects.get(username=req.session['user'])
        product = Plants.objects.get(pk=req.session['pid'])
        amount = product.offer_price * 100  # Razorpay expects amount in paise (1 INR = 100 paise)

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        razorpay_order = client.order.create({
            "amount": amount,
            "currency": "INR",
            "payment_capture": "1"
        })

        order_id = razorpay_order['id']
        order = Order.objects.create(
            name=user.first_name,
            amount=product.offer_price,
            provider_order_id=order_id,
            payment_id='',
            signature_id=''
        )
        order.save()

        return render(
            req, 
            "user/payment.html", 
            {
                "callback_url": "http://127.0.0.1:8000/callback",
                "razorpay_key": settings.RAZORPAY_KEY_ID,
                "order": order,
            }
        )
    else:
        return render(req, 'm_login')

# Callback function after payment
@csrf_exempt
def callback(request):
    def verify_signature(response_data):
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        return client.utility.verify_payment_signature(response_data)

    if "razorpay_signature" in request.POST:
        payment_id = request.POST.get("razorpay_payment_id", "")
        provider_order_id = request.POST.get("razorpay_order_id", "")
        signature_id = request.POST.get("razorpay_signature", "")

        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.signature_id = signature_id

        if not verify_signature(request.POST):
            order.status = PaymentStatus.SUCCESS
            order.save()
            return redirect("book")  # Redirect to a success page or a generic 'book' page

        else:
            order.status = PaymentStatus.FAILURE
            order.save()

            return redirect("book")  # Redirect to a failure page or a generic 'book' page
    else:
        payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
        provider_order_id = json.loads(request.POST.get("error[metadata]")).get("order_id")
        
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.status = PaymentStatus.FAILURE
        order.save()

        return render(request, "callback.html", context={"status": order.status}) 

# Finalize the booking
def book(req):
    if 'user' in req.session:
        address = Address.objects.get(pk=req.session['address'])
        prod = Plants.objects.get(pk=req.session['pid'])
        user = User.objects.get(username=req.session['user'])

        data = Bookings.objects.create(
            user=user,
            pro=prod,
            qty=1,
            price=prod.offer_price,
            address=address
        )
        data.save()

        prod.stock -= 1  # Reduce the stock
        prod.save()

        return redirect(bookings)  # Redirect to the user home page
    else:
        return redirect(m_login)


def bookings(req):
    if 'user' in req.session:
        user=User.objects.get(username=req.session['user'])
        data=Bookings.objects.filter(user=user)[: : -1]
        plants=Plants.objects.all()
        cat=Category.objects.all()
        c_data=Category.objects.all()
        p_data=Plants.objects.all()
        m_data=Main_cat.objects.all()
        return render(req,'user/bookings.html',{'data':data,'cat':cat,'Plants':plants,'c_data':c_data,'p_data':p_data,'m_data':m_data})
    else:
        return redirect(m_login)





    
def view_cart(req):
    if 'user' in req.session:
        user=User.objects.get(username=req.session['user'])
        cart_dtls=Cart.objects.filter(user=user)
        m_data=Main_cat.objects.all()
        c_data=Category.objects.all()
        total=0
        for i in cart_dtls:
            total+=i.price
        return render(req,'user/cart.html',{'cart_dtls':cart_dtls,'total':total,'m_data':m_data,'c_data':c_data})
    else:
        return redirect(m_login)
    
def buyAll(req):
    if 'user' in req.session:
        user=User.objects.get(username=req.session['user'])
        cart=Cart.objects.filter(user=user)
        price=0

        
        for i in cart:
            price+=(i.Plants.offer_price)*i.qty
        total=price
        data=Address.objects.filter(user=user)
        if data:
            # return render(req,'user/orderSummary2.html',{'cart':cart,'data':data,'discount':discount,'price':price,'total':total})
            return redirect(orderSummary2,price=price,total=total)
        else:
            return render(req,"user/addAddress.html")
    else:
        return redirect(m_login) 
    
def orderSummary2(req,price,total):
    if 'user' in req.session:
        user=User.objects.get(username=req.session['user'])
        data=Address.objects.filter(user=user)
        cart=Cart.objects.filter(user=user)
        if req.method == 'POST':
            address=req.POST['address']
            addr=Address.objects.get(user=user,pk=address)
            req.session['address']=addr.pk
            return redirect("payment2")
        else:
            return render(req,'user/cart_buy.html',{'cart':cart,'data':data,'price':price,'total':total})
    else:
        return redirect(m_login)

def payment2(req):
    if 'user' in req.session:
        user = User.objects.get(username=req.session['user'])
        name = user.first_name
        cart=Cart.objects.filter(user=user)
        price=0
        for i in cart:
            price+=(i.Plants.offer_price)*i.qty
        total=price
        amount = total
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        razorpay_order = client.order.create(
            {"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"}
        )
        order_id=razorpay_order['id']
        order = Order.objects.create(
            name=name, amount=amount, provider_order_id=order_id
        )
        order.save()
        return render(
            req,
            "user/payment2.html",
            {
                "callback_url": "http://127.0.0.1:8000/callback2",
                "razorpay_key": settings.RAZORPAY_KEY_ID,
                "order": order,
            },
        )
    else:
        return render(m_login)

@csrf_exempt
def callback2(request):
    def verify_signature(response_data):
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        return client.utility.verify_payment_signature(response_data)

    if "razorpay_signature" in request.POST:
        payment_id = request.POST.get("razorpay_payment_id", "")
        provider_order_id = request.POST.get("razorpay_order_id", "")
        signature_id = request.POST.get("razorpay_signature", "")

        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.signature_id = signature_id
        if  verify_signature(request.POST):
            order.status = PaymentStatus.SUCCESS
            order.save()
            return redirect("book2")  
        else:
            order.status = PaymentStatus.FAILURE
            order.save()
            return redirect("book2")  
 

    else:

        payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
        provider_order_id = json.loads(request.POST.get("error[metadata]")).get(
            "order_id"
        )
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.status = PaymentStatus.FAILURE
        order.save()
        return render(request, "callback.html", context={"status": order.status})  

def book2(req):
    if 'user' in req.session:
        user=User.objects.get(username=req.session['user'])
        address=Address.objects.get(pk=req.session['address'])
        cart=Cart.objects.filter(user=user)
        for i in cart:
            data=Bookings.objects.create(user=i.user,pro=i.Plants,qty=i.qty,price=i.price,address=Address.objects.get(pk=address.pk))
            data.save()
        cart.delete()
        return redirect(bookings)
    else:
        return redirect(m_login)


def deleteBookings(req,pid):
    if 'user' in req.session:
        data=Bookings.objects.get(pk=pid)
        data.delete()
        return redirect(bookings)
    else:
        return redirect(m_login)

def search_suggestions(request):
    query = request.GET.get('query', '').strip()

    if query:
        # Get Plants matching the query, limit the results to 5
        plants = Plants.objects.filter(name__icontains=query)[:5]
        
        suggestions = []
        for plant in plants:
            suggestion = {
                'name': plant.name,
                # 'price': plant.price,
                # 'offer_price': plant.offer_price,
                # 'image': plant.img.url if plant.img else None,  # Image URL (if available)
            }
            suggestions.append(suggestion)
    else:
        suggestions = []

    return JsonResponse({'suggestions': suggestions})

















def manage_orders(req):
    if req.user.is_authenticated and req.user.is_staff:
        orders = Order.objects.all()
        
        if req.method == 'POST':
            order_id = req.POST.get('order_id')
            new_status = req.POST.get('status')
            order = Order.objects.get(id=order_id)
            order.status = new_status
            order.save()
            return redirect('manage_orders')  # Correct the redirect to 'manage_orders' after status update
        
        return render(req, 'admin/manage_orders.html', {'orders': orders})
    else:
        return redirect('m_login') 


def payment(req,pid):
    if 'user' in req.session:
        user=User.objects.get(username=req.session['user'])
        if req.method=='POST':
            user=User.objects.get(username=req.session['user'])
            prdt=Plants.objects.get(pk=pid)
            adrs=Address.objects.get(pk=req.POST['adrs'])
            data=Buy.objects.create(user=user,product=prdt,address=adrs)
            data.save()
            prdt.stock-=1
            prdt.save()
            return redirect(user_home)
        else:
            return redirect(user_home)


# -----------------------------end------------------------
def addrs(req):
    if 'user' in req.session:
        user=User.objects.get(username=req.session['user'])
        data1=Address.objects.filter(user=user)

        if req.method == 'POST':
            user=User.objects.get(username=req.session['user'])
            name=req.POST['name']
            phn=req.POST['phn']
            pin=req.POST['pin']
            loc=req.POST['loc']
            adrs=req.POST['adrs']
            city=req.POST['city']
            state=req.POST['state']
            data=Address.objects.create(user=user,name=name,phn=phn,pin=pin,loc=loc,adrs=adrs,city=city,state=state)
            data.save()
            return redirect(addrs)
        else:
            return render(req,'user/userprf.html',{'data1':data1})
    else:
        return render(req,"user/userprf.html",{'data1':data1})

def delete_address(req,pid):
    if 'user' in req.session:
        data=Address.objects.get(pk=pid)
        data.delete()
        return redirect(addrs)
    else:
        return redirect(user_prfl)


def change_pswd(req):
    if 'user' in req.session:
        if req.method=='POST':
            user=User.objects.get(username=req.session['user'])
            current_password = req.POST['current_password']
            new_password = req.POST['new_password']
            repeat_password = req.POST['repeat_password']
            if new_password==repeat_password:
                if user.check_password(current_password):
                    user.set_password(new_password)
                    user.save()
                    messages.success(req,"Password changed successfully")
                    return redirect(user_logout)
                else:
                    messages.warning(req,"Old password is incorrect")
                    return redirect(change_pswd)
            else:
                messages.warning(req,"Password not matched")
                return redirect(change_pswd)
        else:
            return render(req,'user/change_pswd.html')
    else:
        return redirect(m_login)
    
def mcatgall(req, pid):
    # Retrieve the Main_cat object using the provided id
    main_cat = Main_cat.objects.get(id=pid)
    
    # Retrieve all plants that belong to this Main_cat
    plants = Plants.objects.filter(mcatg=main_cat)
    
    # Pass the plants and main_cat to the template
    return render(req, 'user/mcatgall.html', {'plants': plants, 'main_cat': main_cat})



# -------------admin---------


def add_prd(req):
    if 'admin' in req.session:
        if req.method=='POST':
            p_id=req.POST['p_id']
            name=req.POST['name']
            p_catg=req.POST['p_catg']
            p_dis=req.POST['p_dis']
            price=req.POST['price']
            offer_price=req.POST['offer_price']
            stock=req.POST['stock']
            img= req.FILES['img']
            img2=req.FILES['img2']
            prd_cate=req.POST.get('prd_cate')
            prd_cate2=req.POST.get('prd_cate2')
            cat= Category.objects.get(c_name=prd_cate)
            main_cat = Main_cat.objects.get(m_name=prd_cate2)
            data=Plants.objects.create(p_id=p_id,name=name,p_catg=p_catg,p_dis=p_dis,price=price,offer_price=offer_price,stock=stock,img=img,img2=img2,catg=cat,mcatg=main_cat)
            data.save()
            return redirect(add_prd)
        else:
            data1=Category.objects.all()
            data2=Main_cat.objects.all()
            return render(req,'admin/add_prdct.html',{'data1':data1,'data2':data2})
    else:
        return redirect(m_login)


def admin_home(req):
    
    c_data=Category.objects.all()
    p_data=Plants.objects.all()
    m_data=Main_cat.objects.all()
    return render(req,'admin/adminhome.html',{'c_data':c_data,'p_data':p_data,'m_data':m_data})

def view_prdts(req):
    data=Plants.objects.all()
    return render(req,'admin/view_prdts.html',{'data':data})

def update_prd(req,pid):
    data=Plants.objects.get(pk=pid)
    if req.method=='POST':
        p_id=req.POST['p_id']
        name=req.POST['name']
        p_catg=req.POST['p_catg']
        p_dis=req.POST['p_dis']
        price=req.POST['price']
        offer_price=req.POST['offer_price']
        stock=req.POST['stock']
        img= req.FILES.get('img')
        img2=req.FILES.get('img2')
        if img:
            data=Plants.objects.filter(pk=pid).update(p_id=p_id,name=name,p_catg=p_catg,p_dis=p_dis,price=price,offer_price=offer_price,stock=stock,img=img)
        elif img2:
            data=Plants.objects.filter(pk=pid).update(p_id=p_id,name=name,p_catg=p_catg,p_dis=p_dis,price=price,offer_price=offer_price,stock=stock,img2=img2)
        else:   
            data=Plants.objects.filter(pk=pid).update(p_id=p_id,name=name,p_catg=p_catg,p_dis=p_dis,price=price,offer_price=offer_price,stock=stock)
        return redirect(view_prdts)
    else:
        data1=Category.objects.all()
        data2=Main_cat.objects.all()
        return render(req,'admin/update.html',{'data':data,'data1':data1,'dcta2':data2})
    
def delete_prd(req,pid):
    data=Plants.objects.get(pk=pid)
    url=data.img.url
    og_path=url.split('/')[-1]
    os.remove('media/'+og_path)
    data.delete()
    print(og_path)
    return redirect(view_prdts)






def products(req,pid):
    data=Plants.objects.filter(catg=pid)
    c_data=Category.objects.all()
    return render(req,'user/products.html',{'data':data,'c_data':c_data})
 




