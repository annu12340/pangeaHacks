from django.shortcuts import redirect, render
from .models import Category, Product



def shop_page(request):
    category = Category.objects.all()
    products = Product.objects.filter()
    context = {
        'category': category,
        'products': products
    }
    return render(request, 'shop/dashboard.html', context)


def product_details(request, product_id):
    product_details = Product.objects.get(id=product_id)
    ctg = Category.objects.get(name=product_details.category)
    # related_products = Product.objects.filter(category="ds") 
    related_products = Product.objects.all()#TODO
    context = {
        'product': product_details,
        'related_products': related_products
    }

    return render(request, 'shop/product-details.html', context)


def checkout(request):
    return render(request, 'payment.html')


def successful(request):
    return render(request, 'succesfull.html')

