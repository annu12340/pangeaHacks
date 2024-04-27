import os, requests
import stripe
from django.shortcuts import redirect, render
from .models import Category, Product, CreditCard
from utils.ip_address import get_public_ip
from pangea.config import PangeaConfig
from pangea.services import Audit, UserIntel, Embargo, FileScan, DomainIntel
from pangea.services.intel import HashType
from pangea.tools import logger_set_pangea_config
from pangea.utils import get_prefix, hash_sha256

import pangea.exceptions as pe
from dotenv import load_dotenv

from utils.encrypt_decrypt import encrypt_info, decrypt_info

load_dotenv()
config = PangeaConfig(domain=os.getenv("PANGEA_DOMAIN"))
audit = Audit(os.getenv("PANGEA_TOKEN"), config=config)
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


def shop_page(request):
    print("request.user.is_authenticated", request.user.is_authenticated)
    category = Category.objects.all()
    products = Product.objects.all()
    context = {"category": category, "products": products}
    # audit.log(f"User has visited shop page")
    return render(request, "shop/dashboard.html", context)


def product_details(request, product_id):
    product_details = Product.objects.get(id=product_id)
    related_products = Product.objects.get(category=product_details.category)
    context = {"product": product_details, "related_products": related_products}

    return render(request, "shop/product-details.html", context)


def checkout(request, product_id):
    # Check if the user has any saved cards
    user_cards = CreditCard.objects.filter(user_id=request.user.id)
    print("inside checkout aaa", user_cards)
    if user_cards.exists():
        # If user has saved cards, display the list of cards
        return render(request, "payment/card_list.html", {"cards": user_cards})

    else:
        # If user doesn't have any saved cards, prompt them to add a new card
        print("Adding new card")
        return redirect("new_card", product_id=product_id)


def new_card(request, product_id):
    if request.POST:
        print("possting", request.POST)

        card_number = request.POST["card_num"]
        cardholder_name = request.POST.get("card_holder", "")
        expiry_date = request.POST.get("card_expiry_date", "")
        security_number = request.POST.get("card_cvv", "")
        encryption_key = request.POST.get("encryption_key")
        # if encryption_key:
        # Encrpting and ciphering sensitive card info
        # TODO: Rwmove comment
        # card_number=encrypt_info(card_number, encryption_key)
        # security_number=encrypt_info(card_number, encryption_key)
        card_number = card_number
        security_number = security_number
        card_info = CreditCard(
            card_number=card_number,
            cardholder_name=cardholder_name,
            expiry_date=expiry_date,
            security_number=security_number,
            user_id=request.user.id,
            encryption_key=encryption_key,
        )

        card_info.save()
        print("redircting to list_cards")
        return redirect("list_cards", product_id=product_id)
    else:
        return render(request, "payment/add_new_card.html", {"product_id": product_id})


def list_cards(request, product_id):
    print("reached here")
    product = Product.objects.filter(id=product_id)[0]
    print("productsproductsproducts", product.name)

    user_cards = CreditCard.objects.filter(user_id=request.user.id)
    return render(
        request,
        "payment/card_list.html",
        {"cards": user_cards, "product": product},
    )


def check_password(request, redirect_type):
    return render(request, "payment/password.html")


def payment(request, product_id):
    ip_addr = get_public_ip()
    sanction_msg = ""
    token = os.getenv("PANGEA_TOKEN")
    domain = os.getenv("PANGEA_DOMAIN")
    config = PangeaConfig(domain=domain)
    # embargo = Embargo(token, config=config, logger_name="embargo")
    # logger_set_pangea_config(logger_name=embargo.logger.name)

    try:
        # embargo_response = embargo.ip_check(ip=ip_addr)
        # print(f"Response: {embargo_response.result}")
        # audit.log(f"A user with ip addresss {ip_addr} has tried to login")
        # sanctions_count= embargo_response.result.count
        sanctions_count = 0
        if sanctions_count >= 1:
            print("sanction_msg", sanction_msg)
            # sanction_msg=embargo_response.result.summary
    except pe.PangeaAPIException as err:
        print(f"Embargo Request Error: {err.response.summary}")
        for er in err.errors:
            print(f"\t{er.detail} \n")

    return render(request, "succesfull.html")
