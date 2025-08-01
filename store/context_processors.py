from .models import Category
from orders.models import Cart

def categories(request):
    return {
        'categories': Category.objects.filter(is_active=True)
    }

def cart_count(request):
    count = 0
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            count = cart.get_total_items()
        except Cart.DoesNotExist:
            count = 0
    return {'cart_count': count}