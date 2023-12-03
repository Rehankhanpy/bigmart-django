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
       path('search/', views.search, name='search'),
       path('category/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),

]