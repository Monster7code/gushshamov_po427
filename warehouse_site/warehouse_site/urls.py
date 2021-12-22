"""warehouse_site URL Configuration

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
from app_warehouse.views import *
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainPage.as_view()),
    path('order_page.html/', Order_Page.as_view()),
    path('personal_area.html', Personal_area.as_view()),
    path('page_registr.html', Page_registr.as_view()),
    path('page_log_in.html', Page_login.as_view()),
    path('page_warehouses.html/<int:id>', Page_warehouses.as_view()),
    path('page_payback.html/<int:id>', Page_payback.as_view()),
    path('order_page_2.html/', Order_Page_2.as_view())
]
