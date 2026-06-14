# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.home, name='home'),
#     path('login/', views.login_view, name='login'),  # New login URL
#     path('register/customer/', views.register_customer, name='register_customer'),
#    path('register/retailer/', views.register_retailer, name='register_retailer'), 
#     path('manufacturer/dashboard/', views.manufacturer_dashboard, name='manufacturer_dashboard'),
#     path('distributor/dashboard/', views.distributor_dashboard, name='distributor_dashboard'),
#     path('retailer/dashboard/', views.retailer_dashboard, name='retailer_dashboard'),
#     path('customer/dashboard/', views.customer_dashboard, name='customer_dashboard'),
#     path('manufacturer/add_product/', views.add_product, name='add_product'),  # 🔧 ADDED

# ]


from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/customer/', views.register_customer, name='register_customer'),
    path('register/retailer/', views.register_retailer, name='register_retailer'),
    path('manufacturer/dashboard/', views.manufacturer_dashboard, name='manufacturer_dashboard'),
    path('manufacturer/add_product/', views.add_product, name='add_product'),
    path('manufacturer/edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('manufacturer/delete_product/<int:product_id>/', views.delete_product, name='delete_product'),  # 🔧 ADDED
    path('distributor/dashboard/', views.distributor_dashboard, name='distributor_dashboard'),
    path('retailer/dashboard/', views.retailer_dashboard, name='retailer_dashboard'),
    path('customer/dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('manufacturer/register_distributor/', views.register_distributor, name='register_distributor'),
    path('distributor/dashboard/', views.distributor_dashboard, name='distributor_dashboard'),
    path('distributor/add_stock/<int:product_id>/', views.add_to_distributor_stock, name='add_to_distributor_stock'),
    path('distributor/edit_stock/<int:stock_id>/', views.edit_distributor_stock, name='edit_distributor_stock'),
    path('distributor/add_more/<int:stock_id>/', views.add_more_stock, name='add_more_stock'),
    path('retailer/add_product/', views.retailer_add_product, name='retailer_add_product'), 
    path('retailer/add_stock/<int:stock_id>/', views.add_to_retailer_stock, name='add_to_retailer_stock'),
    path('buy/<int:product_id>/', views.buy_product, name='buy_product'),
    path('retailer/confirm_stock/<int:stock_id>/', views.confirm_retailer_stock, name='confirm_retailer_stock'),
    path('distributor/confirm_stock/<int:product_id>/', views.confirm_distributor_stock, name='confirm_distributor_stock'),



]

# Media serving
from django.conf import settings
from django.conf.urls.static import static
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
