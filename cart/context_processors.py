from .models import Cart

def cart_count(request):
    cart_item_count = 0
    if request.user.is_authenticated:
        cart_item_count = Cart.objects.filter(user=request.user).count()

    return {'cart_item_count': cart_item_count}