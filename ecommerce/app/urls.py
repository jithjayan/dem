from django.urls import path
from . import views


urlpatterns=[
    path('m_login',views.m_login),
    path('reg',views.reg),
    path('admin_home',views.admin_home),
    path('',views.user_home),
    path('int_plt',views.int_plt),
    path('user_prfl',views.user_prfl),
    path('user_logout',views.user_logout),
    path('homep',views.homep),
    path('add_to_cart/<pid>',views.add_to_cart),
    path('delete_cart/<pid>',views.delete_cart),
    path('view_cart',views.view_cart),
    path('view_pro/<pid>',views.view_pro),
    path('add_catg',views.add_catg),
    path('admin_logout',views.admin_logout),
    path('buy',views.buy),
    path('adrs',views.addrs),
    path('delete_address/<pid>',views.delete_address),
    path('add_prd',views.add_prd),
    path('add_Mcatg',views.add_Mcatg),
    path('products/<pid>',views.products),
    path('view_prdts',views.view_prdts),
    path('update_prd/<pid>',views.update_prd),
    path('delete_prd/<pid>',views.delete_prd),
    path('search',views.search),

    # path('view_category',views.view_category),
 

]