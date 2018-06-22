'''from django.urls import path'''
from canteen_new_app.views import aboutus,chinese,sandwich,cart,remove,bill,product_info,addstudentinfo,signup,home,login,auth_view,logout,loggedin,invalidlogin,cart_display
from django.contrib.auth import views as auth_views
from django.conf.urls import url

urlpatterns=[
        url(r'^signup/$',signup),
        url(r'^home/$',home),
        url(r'^login/$',login),
        url(r'^auth/$',auth_view),
        url(r'^logout/$',logout),
        url(r'^loggedin/$',loggedin),
        url(r'^invalidlogin/$',invalidlogin),
        url(r'^addstudentinfo/$',addstudentinfo),
        url(r'^product_info/$',product_info),
        url(r'^cart/$',cart),
        url(r'^cart_display/$',cart_display),
        url(r'^remove/$',remove),
        url(r'^bill/$',bill),
        url(r'^sandwich/$',sandwich),
        url(r'^chinese/$',chinese),
        url(r'^aboutus/$',aboutus),
]
#urls.py
