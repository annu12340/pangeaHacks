import os
from django.shortcuts import redirect, render
from .models import Category, Product, CreditCard
from pangea.config import PangeaConfig
from pangea.services import Audit, UserIntel, Embargo, FileScan, DomainIntel
from pangea.services.intel import HashType
from pangea.tools import logger_set_pangea_config
from pangea.utils import get_prefix, hash_sha256
from pangea.services.vault.vault import Vault
import pangea.exceptions as pe
from dotenv import load_dotenv


load_dotenv()
config = PangeaConfig(domain=os.getenv("PANGEA_DOMAIN"))  
audit = Audit(os.getenv("PANGEA_TOKEN"), config=config) 


def shop_page(request):
    category = Category.objects.all()
    products = Product.objects.filter()
    context = {
        'category': category,
        'products': products
    }
    # audit.log(f"User has visited shop page")
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


def checkout(request, product_id):
    # Check if the user has any saved cards
    user_cards = CreditCard.objects.filter(user_id=request.user.id)
    print(user_cards)
    if user_cards.exists():
        # If user has saved cards, display the list of cards
        return render(request, 'payment/card_list.html', {'cards': user_cards})
    
    else:
        # If user doesn't have any saved cards, prompt them to add a new card
        print("Adding new card")
        return redirect('new_card',product_id=product_id)

def new_card(request, product_id):
    if request.POST:
        print("possting",request.POST)
        
        card_number = request.POST['card_num']
        print("card_numbercard_numbercard_numbercard_number",card_number)
        cardholder_name = request.POST.get('card_holder', '')
        expiry_date = request.POST.get('card_expiry_date', '')
        security_number = request.POST.get('card_cvv', '')
        card_info = CreditCard(
            card_number=card_number,
            cardholder_name=cardholder_name,
            expiry_date=expiry_date,
            security_number=security_number,
            user_id=request.user.id
        )
        

        card_info.save()
        return redirect('success')
   
    return render(request, 'payment/add_new_card.html', {'product_id': product_id})

def success(request):
    return render(request, 'succesfull.html')

