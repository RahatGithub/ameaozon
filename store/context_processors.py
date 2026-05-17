from django.core.cache import cache
from .models import Category
from orders.models import Cart

def categories(request):
    cats = cache.get('active_categories')
    if cats is None:
        cats = list(Category.objects.filter(is_active=True))
        cache.set('active_categories', cats, 300)  # cache for 5 minutes
    return {'categories': cats}

def cart_count(request):
    count = 0
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            count = cart.get_total_items()
        except Cart.DoesNotExist:
            count = 0
    return {'cart_count': count}

def cart_items_map(request):
    cart_map = {}
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_map = dict(cart.items.values_list('product_id', 'quantity'))
        except Cart.DoesNotExist:
            pass
    return {'cart_items_map': cart_map}