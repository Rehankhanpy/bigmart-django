from .models import *
from .views import _cart_id

def menu_links(request):
       links = category.objects.all()
       return dict(links=links)


def cart_counter(request):
       cart_count = 0
       if 'admin'in request.path:
              return {}
       else:
              try:
                     Cart = cart.objects.filter(cart_id=_cart_id(request))
                     if request.user.is_authenticated:
                            cart_items = cartitem.objects.all().filter(user=request.user)
                     else:
                            cart_items = cartitem.objects.all().filter(cart=Cart[:1])
                     for cart_item in cart_items:
                            cart_count += 1
              except cart.DoesNotExist:
                     cart_count = 0
       return dict(cart_count=cart_count)
              