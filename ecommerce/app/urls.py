from django.urls import path
from . import views


urlpatterns=[
    path('m_login',views.m_login),
    path('reg',views.reg),

    path('verify_otp',views.verify_otp),
    path('resend',views.resend_otp),
    path('forget',views.forgetpassword),
    path('reset',views.resetpassword),
    path('verify_otp_reg',views.verify_otp_reg),
    path('resend_otp_reg',views.resend_otp_reg ),


    path('admin_home',views.admin_home),
    path('',views.user_home),
    path('int_plt',views.int_plt),
    path('user_prfl',views.user_prfl),
    path('user_logout',views.user_logout),
    path('homep',views.homep),
    path('a_home',views.a_home),
    path('add_to_cart/<pid>',views.add_to_cart),
    path('delete_cart/<pid>',views.delete_cart),
    path('view_cart',views.view_cart),
    path('view_pro/<pid>',views.view_pro),
    # path('add_catg',views.add_catg),
    path('admin_logout',views.admin_logout),
    path('buy/<pid>',views.buy),
    path('adrs',views.addrs),
    path('delete_address/<pid>',views.delete_address),
    path('add_prd',views.add_prd),
    path('add_Mcatg',views.add_Mcatg),
    path('edit_Mcatg/<pid>',views.edit_Mcatg),
    path('delete_Mcatg/<pid>',views.delete_Mcatg),
    path('edit_catg/<pid>',views.edit_catg),
    path('delete_catg/<pid>',views.delete_catg),
    path('products/<pid>',views.products),
    path('view_prdts',views.view_prdts),
    path('update_prd/<pid>',views.update_prd),
    path('delete_prd/<pid>',views.delete_prd),
    path('cartIncrement/<pid>',views.cartIncrement),
    path('cartDecrement/<pid>',views.cartDecrement),
    path('search',views.search),
    path('change_pswd',views.change_pswd),
    path('mcatgall/<pid>',views.mcatgall),
    path('payment/<pid>',views.payment),
    path('manage_orders/', views.manage_orders,name='manage_orders'),
    path('cart_buy', views.cart_buy, name='cart_buy'),
    # path('view_category',views.view_category),
 

]