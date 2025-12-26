from django.shortcuts import render

from shop.models import Product, ProductImage


def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def shop(request):
    return render(request, 'shop.html')

def shop_single_product(request, pk):
    product = Product.objects.get(pk=pk)
    product_images = ProductImage.objects.filter(product=product)

    return render(request, 'shop-single-product.html', {'product': product, 'product_images': product_images})

def shop_checkout(request):
    return render(request, 'shop-checkout.html')