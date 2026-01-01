from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from shop.models import Product, Category
from .models import Cart, CartItem, Order, OrderItem
from decimal import Decimal


def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).order_by('-created_at').first()
        if not cart:
            cart = Cart.objects.create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        cart, created = Cart.objects.get_or_create(session_key=request.session.session_key)
    return cart


def cart_view(request):
    categories = Category.objects.all()
    cart = get_or_create_cart(request)
    return render(request, 'cart.html', {
        'cart': cart,
        'categories': categories
    })


def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart = get_or_create_cart(request)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f'Updated {product.name} quantity in cart')
    else:
        messages.success(request, f'Added {product.name} to cart')

    return redirect('cart:view')


def update_cart(request, pk):
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, pk=pk, cart=cart)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Cart updated successfully')
        else:
            cart_item.delete()
            messages.success(request, 'Item removed from cart')

    return redirect('cart:view')


def remove_from_cart(request, pk):
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, pk=pk, cart=cart)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.success(request, f'Removed {product_name} from cart')
    return redirect('cart:view')


def clear_cart(request):
    cart = get_or_create_cart(request)
    cart.items.all().delete()
    messages.success(request, 'Cart cleared')
    return redirect('cart:view')


def process_checkout(request):
    if request.method != 'POST':
        return redirect('shop:shop_checkout')

    cart = get_or_create_cart(request)

    if not cart or not cart.items.exists():
        messages.error(request, 'Your cart is empty')
        return redirect('cart:view')

    email = request.POST.get('email', '')
    first_name = request.POST.get('first_name', '')
    last_name = request.POST.get('last_name', '')
    address = request.POST.get('address', '')
    apartment = request.POST.get('apartment', '')
    city = request.POST.get('city', '')
    country = request.POST.get('country', '')
    postal_code = request.POST.get('postal_code', '')

    if not all([email, last_name, address, city, country, postal_code]):
        messages.error(request, 'Please fill in all required fields')
        return redirect('shop:shop_checkout')

    subtotal = cart.get_total()
    shipping_cost = Decimal('10.00')
    total = subtotal + shipping_cost

    # Create the order
    order = Order.objects.create(
        user=request.user if request.user.is_authenticated else None,
        order_number=Order.generate_order_number(),
        email=email,
        first_name=first_name,
        last_name=last_name,
        address=address,
        apartment=apartment,
        city=city,
        country=country,
        postal_code=postal_code,
        subtotal=subtotal,
        shipping_cost=shipping_cost,
        total=total,
        status='shipped'
    )

    for cart_item in cart.items.all():
        price = cart_item.product.discount_price if cart_item.product.discount_price else cart_item.product.price
        OrderItem.objects.create(
            order=order,
            product=cart_item.product,
            product_name=cart_item.product.name,
            product_sku=cart_item.product.sku or '',
            quantity=cart_item.quantity,
            price=price
        )

    cart.items.all().delete()

    messages.success(request, f'Order {order.order_number} has been placed successfully!')
    return redirect('cart:order_confirmation', order_number=order.order_number)


def order_confirmation(request, order_number):

    order = get_object_or_404(Order, order_number=order_number)
    categories = Category.objects.all()

    return render(request, 'order-confirmation.html', {
        'order': order,
        'categories': categories
    })

