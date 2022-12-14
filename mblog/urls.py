"""mblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.contrib.staticfiles.views import serve
from mainsite.views import homepage,showpost
from About.views import about,listing,disp_detail,matpshow
from kmesns.views import kmeanshow


urlpatterns = [
    path('admin/', admin.site.urls),
    path('favicon.ico',serve,{'path':'img/auo.ico'}),
    path('',homepage),
    path('post/<slug:slug>/',showpost),
    path('about/',about),
    path('list/',listing),
    path('list/<str:id>',disp_detail),
    path('matp/<str:slug>/',matpshow),
    path('kmeans/<str:slug>/',kmeanshow),
]
