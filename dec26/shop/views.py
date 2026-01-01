from django.db.models import Prefetch
from django.shortcuts import render, redirect

from shop.models import Product, ProductImage, Category


def home(request):
    categories = Category.objects.all()

    primary_image_qs = ProductImage.objects.filter(is_primary=True)

    latest_products = Product.objects.prefetch_related(
        Prefetch(
            'images',
            queryset=primary_image_qs,
            to_attr='primary_img_cache',
        )
    ).order_by('-created_at')[:8]

    featured_products = Product.objects.prefetch_related(
        Prefetch(
            'images',
            queryset=primary_image_qs,
            to_attr='primary_img_cache',
        )
    ).filter(discount_price__isnull=False).order_by('-discount_percentage')[:8]

    if not featured_products:
        featured_products = Product.objects.prefetch_related(
            Prefetch(
                'images',
                queryset=primary_image_qs,
                to_attr='primary_img_cache',
            )
        )[:8]

    return render(request, 'index.html', {
        "categories": categories,
        "latest_products": latest_products,
        "featured_products": featured_products,
    })

def about(request):
    categories = Category.objects.all()
    return render(request, 'about.html', {"categories": categories})

def contact(request):
    categories = Category.objects.all()
    return render(request, 'contact.html', {"categories": categories})

def shop(request):
    categories = Category.objects.all()
    primary_image_qs = ProductImage.objects.filter(is_primary=True)

    products = Product.objects.prefetch_related(
        Prefetch(
            'images',
            queryset=primary_image_qs,
            to_attr='primary_img_cache',
        )
    ).all()

    return render(request, 'shop.html', {
        "categories": categories,
        "products": products
    })

def shop_single_product(request, pk):
    product = Product.objects.get(pk=pk)
    product_images = ProductImage.objects.filter(product=product)
    categories = Category.objects.all()

    primary_image_qs = ProductImage.objects.filter(is_primary=True)
    related_products = Product.objects.filter(
        category=product.category
    ).exclude(pk=product.pk).prefetch_related(
        Prefetch(
            'images',
            queryset=primary_image_qs,
            to_attr='primary_img_cache',
        )
    )[:4]

    return render(request, 'shop-single-product.html', {
        'product': product,
        'product_images': product_images,
        'categories': categories,
        'related_products': related_products
    })

def shop_checkout(request):
    categories=Category.objects.all()
    return render(request, 'shop-checkout.html', {"categories": categories})

def category(request, pk):
    primary_image_qs = ProductImage.objects.filter(is_primary=True)
    categories = Category.objects.all()
    products = Product.objects.filter(category__pk=pk).prefetch_related(
        Prefetch(
            'images',
            queryset=primary_image_qs,
            to_attr='primary_img_cache',
        )
    )

    return render(request, 'shop-products.html', {'products': products, "categories": categories})
