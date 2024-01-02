from django.urls import path
from . import views

urlpatterns = [
       path('', views.index, name='index'),
       path('store', views.store, name='store'),
       path('category/<slug:category_slug>/', views.store, name='products_by_category'),
       path('add_cart/<int:product_id>/', views.add_cart, name='add_cart'),
       path('remove_cart/<int:product_id>/<int:cart_item_id>/', views.remove_cart, name='remove_cart'),
       path('remove_cart_item/<int:product_id>/<int:cart_item_id>/', views.remove_cart_item, name='remove_cart_item'),
       path('Cart', views.Cart, name='Cart'),
       path('dashboard', views.dashboard, name='dashboard'),
       path('forgotPassword', views.forgotPassword, name='forgotPassword'),
       path('resetPassword', views.resetPassword, name='resetPassword'),
       path('register/', views.register, name='register'),
       path('login/', views.login, name='login'),
       path('activate/<uidb64>/<token>', views.activate, name='activate'),
       path('resetpassword_validate/<uidb64>/<token>', views.resetpassword_validate, name='resetpassword_validate'),
       path('logout/', views.logout, name='logout'),
       path('search/', views.search, name='search'),
       path('category/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),

]