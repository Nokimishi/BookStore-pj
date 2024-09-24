from django.contrib import admin
from django.urls import path,include,re_path
from django.conf.urls.static import static 
from django.conf import settings
from django.shortcuts import redirect
from book_store3.views import *
from django.views.generic import TemplateView
urlpatterns = [
    path('', lambda request: redirect('/book/home')),
    path('admin/', admin.site.urls),
    path('login/', mylogin, name="login"),
    path('logout/', mylogut),
    path('forgot_password/', forgot_password, name='forgot_password'),
    path('reset_password/<int:user_id>/', reset_password, name='reset_password'),
    path('register/', myregister),
    path('book/',include('book_store3.urls')),
    path('profile/', profile, name="profile"),
    path('userprofile_create/', userprofile_create, name="userprofile_create"),
    path('profile/edit/', userprofile_edit, name='userprofile_edit'),
    re_path(r'^.*/$', pagenotfound),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
