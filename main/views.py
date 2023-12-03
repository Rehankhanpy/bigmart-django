from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.http import HttpResponse
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q

# Create your views here.
def index(request):
       context = {
              'banner':banner.objects.all(),
              'categories':category.objects.all(),
              'products':Product.objects.filter(is_available=True)

       }

       return render(request, 'index.html', context)



def store(request, category_slug=None):
       categories = None
       products = None

       if category_slug != None:
              categories = get_object_or_404(category, slug=category_slug)
              products = Product.objects.filter(category=categories, is_available=True)
              paginator = Paginator(products, 2)
              page = request.GET.get('page')
              paged_products = paginator.get_page(page)
              product_count = products.count()
       else: 
              products = Product.objects.all().filter(is_available=True).order_by('id')
              paginator = Paginator(products, 2)
              page = request.GET.get('page')
              paged_products = paginator.get_page(page)
              product_count = products.count()
       context = {
              'products':paged_products,
              'product_count':product_count,
       }

       return render(request, 'store.html', context)

def product_detail(request, category_slug, product_slug):
       try:
              single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
              in_cart = cartitem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
              
              

       except Exception as e:
              raise e
       
       context = {
              'single_product':single_product,
              'in_cart':in_cart,
             
       }

       return render(request, 'product_detail.html', context)



def _cart_id(request):
       Cart = request.session.session_key
       if not Cart:
              Cart = request.session.create()
       return Cart

def add_cart(request, product_id):
       product = Product.objects.get(id=product_id)
       product_variation = []

       if request.method == 'POST':
              for item in request.POST:
                     key = item
                     value = request.POST[key]

                     try:
                            Variation = variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                            product_variation.append(Variation)
                     
                     except:
                            pass

       try:
              Cart = cart.objects.get(cart_id=_cart_id(request))
              
       except cart.DoesNotExist:
              Cart = cart.objects.create(
                     cart_id = _cart_id(request),

              )
       Cart.save()

       does_cart_item_exist = cartitem.objects.filter(product=product, cart=Cart).exists()
       if does_cart_item_exist:
              cart_item = cartitem.objects.filter(product=product, cart=Cart)
              print(cart_item)
              # existing variations -> database
              # current variations -> product variation
              # item_id -> database
              existing_variations_list = []
              cart_item_id = []
              for item in cart_item:
                     existing_variation = item.variations.all()
                     existing_variations_list.append(list(existing_variation))
                     cart_item_id.append(item.id)
              
              if product_variation in existing_variations_list:
                     # increse the cart item quantity
                     index = existing_variations_list.index(product_variation)
                     item_id = cart_item_id[index]
                     item = cartitem.objects.get(product=product, id=item_id)
                     item.quantity += 1
                     item.save()

              else:
                     item = cartitem.objects.create(
                            product = product,
                            quantity = 1,
                            cart = Cart, 
                     )
                     if len(product_variation) > 0:
                            item.variations.clear()
                            item.variations.add(*product_variation)
                     item.save()

       else:
              cart_item = cartitem.objects.create(
                     product = product,
                     quantity = 1,
                     cart = Cart,
              )
              if len(product_variation) > 0:
                     cart_item.variations.clear()
                     cart_item.variations.add(*product_variation)
              cart_item.save()
       return redirect('Cart')


def remove_cart(request, product_id, cart_item_id):
       Cart = cart.objects.get(cart_id=_cart_id(request))
       product = get_object_or_404(Product, id=product_id)
       try:
              cart_item = cartitem.objects.get(product=product, cart=Cart, id=cart_item_id)
              if cart_item.quantity > 1:
                     cart_item.quantity -= 1
                     cart_item.save()
              else:
                     cart_item.delete()
       except:
              pass
       return redirect('Cart')


def remove_cart_item(request, product_id, cart_item_id):
       Cart = cart.objects.get(cart_id=_cart_id(request))
       product = get_object_or_404(Product, id=product_id)
       cart_item = cartitem.objects.get(product=product, cart=Cart, id=cart_item_id)
       cart_item.delete()
       return redirect('Cart')


def Cart(request, total=0, quantity=0, cart_items=None):
       try:
              Cart = cart.objects.get(cart_id=_cart_id(request))
              cart_items = cartitem.objects.filter(cart=Cart, is_active=True)
              for cart_item in cart_items:
                     total += (cart_item.product.price * cart_item.quantity)
                     quantity = cart_item.quantity

              tax = (3 * total)/100
              grand_total = total + tax

       except ObjectNotExist:
              pass

       context = {
              "total":total,
              "quantity":quantity,
              "cart_items":cart_items,
              "grand_total":grand_total,
              "tax":tax,
       }

       return render(request, 'cart.html', context)


def search(request):
       if 'keyword' in request.GET:
              keyword = request.GET['keyword']
              if keyword:
                     products = Product.objects.order_by('-created_date').filter(Q(name__icontains=keyword) | Q(description__icontains=keyword))
                     product_count = products.count()

       context = {
              'products':products,
              'product_count':product_count,
       }

       return render(request, 'store.html', context)

















































