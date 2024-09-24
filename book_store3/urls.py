from django.urls import path
from book_store3.views import *

urlpatterns = [
    path('list/',booklist,name='booklist'), 
    path('home/',home), 
    path('create/',bookcreate), 
    path('detail/<int:b_id>/',bookdetail),  
    path('cartCreate/<int:pdt_id>/', CartCreate),
    path('cartList/', CartList),
    path('cartDelete/<int:cart_id>/', CartDelete),
    path('cartOrderCreate/', cartOrderCreate),
    path('buyNow/<int:post_id>/', buyNow),
    path('orderList/', orderList),
    path('orderDelete/<str:order_id>/', orderDelete),
    path('delete/<int:b_id>/', bookdelete),
    path('edit/<int:b_id>/', bookedit),
    path('contact/', bookcontact, name='contact'),
    path('navigate/', navigate),
    ]
