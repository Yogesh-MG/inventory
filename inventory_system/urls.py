# inventory_system/urls.py
from django.contrib import admin
from django.urls import path, include
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),	
    path('', views.index, name='index'),
    path('login/', views.CustomLoginView.as_view(), name='login'),  # Ensure this line exists
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('purchase/', views.add_purchase, name='add_purchase'),
    path('sale/', views.add_sale, name='add_sale'),
    path('stock/', views.stock_list, name='stock_list'),
    path('bills/', views.bill_summary, name='bill_summary'),
    path('seller/update/<int:pk>/', views.SellerUpdateView.as_view(), name='update_seller'),
    path('goods/update/<int:pk>/', views.GoodsUpdateView.as_view(), name='update_goods'),
    path('buyer/update/<int:pk>/', views.BuyerUpdateView.as_view(), name='update_buyer'),
    path('seller/add/', views.SellerCreateView.as_view(), name='add_seller'),
    path('goods/add/', views.GoodsCreateView.as_view(), name='add_goods'),
    path('buyer/add/', views.BuyerCreateView.as_view(), name='add_buyer'),
]
