from .models import Cart


def cart_context(request):
    cart = None
    cart_items = []
    cart_item_count = 0
    cart_total = 0

    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).order_by('-created_at').first()
    else:
        if request.session.session_key:
            cart = Cart.objects.filter(session_key=request.session.session_key).first()

    if cart:
        cart_items = cart.items.all()
        cart_item_count = cart.total_items
        cart_total = cart.get_total()

    return {
        'cart': cart,
        'cart_items': cart_items,
        'cart_item_count': cart_item_count,
        'cart_total': cart_total,
    }

