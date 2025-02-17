from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from .models import *
import os
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

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


def reg(req):
        if req.method=='POST':
            name=req.POST['name']
            email=req.POST['email']
            password=req.POST['password']
            try:
                send_mail('user registration', 'account created', settings.EMAIL_HOST_USER, [email])
                data=User.objects.create_user(first_name=name,email=email,password=password,username=email)
                data.save()
                return redirect(m_login)
            except:
                messages.warning(req,"Email not valid")
                return redirect(reg)
        else:
            return render(req,'user/register.html')

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

def view_pro(req,pid):
    data=Plants.objects.get(pk=pid)
    
    return render(req,'user/view_pro.html',{'data':data})

def add_to_cart(req,pid):
    if 'user' in req.session:
        prdct=Plants.objects.get(pk=pid)
        user=User.objects.get(username=req.session['user'])

        try:

            data=Cart.objects.create(user=user,Plants=prdct)
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
        total=0
        for i in cart_dtls:
            total+=i.price
        return render(req,'user/cart.html',{'cart_dtls':cart_dtls,'total':total})
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
    # else:
    #     return redirect(m_login)
    
# def add_catg(req):
#     data2=Category.objects.all()

#     if req.method=='POST':
#         prd_c=req.POST['prd_c']
#         name=req.POST['c_name']
#         data=Category.objects.create(m_cat=Main_cat.objects.get(m_name=prd_c),c_name=name)
#         main_cat = Main_cat.objects.get(m_name=prd_c)
#         data = Category.objects.create(m_cat=main_cat, c_name=name)
#         data.save()
#         return render(req,'admin/add_catg.html',{'data':data,'data2':data2})
#     else:
#         data1=Main_cat.objects.all()
#         return render(req,'admin/add_catg.html',{'Main_cat':data1})

# def catg(req):
#     if req.method=='POST':
#         name=req.POST['m_name']
#         data=Main_cat.objects.create(m_name=name)
#         data.save()
#         return redirect(add_Mcatg)
#     else:
#         data=Category.objects.all()
#         data1=Main_cat.objects.all()
#         return render(req,'admin/add_Mcatg.html',{'Category':data,'Main_cat':data1})
    
# def add_catg(req):
#     data2=Category.objects.all()

#     if req.method=='POST':
#         prd_c=req.POST['prd_c']
#         name=req.POST['c_name']
#         # data=Category.objects.create(m_cat=Main_cat.objects.get(m_name=prd_c),c_name=name)
#         main_cat = Main_cat.objects.get(m_name=prd_c)
#         data = Category.objects.create(m_cat=main_cat, c_name=name)
#         data.save()
#         return render(req,'admin/add_catg.html',{'data':data,'data2':data2})
#     else:
#         data1=Main_cat.objects.all()
#         return render(req,'admin/add_catg.html',{'Main_cat':data1})

def buy(req,pid):
    if 'user' in req.session:
        user=User.objects.get(username=req.session['user'])
        prdt=Plants.objects.get(pk=pid)
        data=Address.objects.filter(user=user)
        return render(req,'user/buy.html',{'data':data,'prdt':prdt})
    else:
        return redirect(m_login)






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
                    return redirect(change_pswd)
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
            prd_cate=req.POST['prd_cate']
            prd_cate2=req.POST['prd_cate2']
            cat = Category.objects.get(c_name=prd_cate)
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
        img= req.FILES['img']
        img2=req.FILES['img2']
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
    if 'user' in req.session:
        data=Plants.objects.filter(catg=pid)
        c_data=Category.objects.all()
        return render(req,'user/products.html',{'data':data,'c_data':c_data})
    else:
        return redirect(m_login)






