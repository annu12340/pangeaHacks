import os, requests
import stripe
from django.urls import reverse
from django.shortcuts import redirect, render
from .models import Category, Product, CreditCard
from qrcode.models import Qrcode_info
from utils.ip_address import get_public_ip
from pangea.config import PangeaConfig
from pangea.services import Audit, UserIntel, Embargo, FileScan, DomainIntel, IpIntel
from pangea.services.intel import HashType
from pangea.tools import logger_set_pangea_config
from pangea.utils import get_prefix, hash_sha256
from pangea.services.intel import IPDomainData, IPGeolocateData, IPProxyData, IPVPNData

import pangea.exceptions as pe
from dotenv import load_dotenv

from utils.encrypt_decrypt import encrypt_info, decrypt_info

load_dotenv()
config = PangeaConfig(domain=os.getenv("PANGEA_DOMAIN"))
audit = Audit(os.getenv("PANGEA_TOKEN"), config=config)
embargo=Embargo(os.getenv("PANGEA_TOKEN"), config=config)
token = os.getenv("PANGEA_TOKEN")

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


def shop_page(request):
    category = Category.objects.all()
    products = Product.objects.all()
    context = {"category": category, "products": products}
    audit.log(f"User {request.user.name} has visited shop page")
    return render(request, "shop/dashboard.html", context)


def product_details(request, product_id):
    product_details = Product.objects.get(id=product_id)
    related_products = Product.objects.filter(category=product_details.category)
    context = {"product": product_details, "related_products": related_products}

    return render(request, "shop/product-details.html", context)


def checkout(request, product_id):
    # Check if the user has any saved cards
    user_cards = CreditCard.objects.filter(user_id=request.user.id)

    if user_cards.exists():
        # If user has saved cards, display the list of cards
        audit.log(f"Displaying user's saved credit card info")
        return render(request, "payment/card_list.html", {"cards": user_cards})

    else:
        # If user doesn't have any saved cards, prompt them to add a new card
        audit.log("Adding new card for the user")
        return redirect("new_card", product_id=product_id)


def new_card(request, product_id):
    if request.POST:
  
        card_number = request.POST["card_num"]
        cardholder_name = request.POST.get("card_holder", "")
        expiry_date = request.POST.get("card_expiry_date", "")
        security_number = request.POST.get("card_cvv", "")
        encryption_key = request.POST.get("encryption_key")
        if encryption_key:
        # Encrpting and ciphering sensitive card info
            card_number=encrypt_info(card_number, encryption_key)
            security_number=encrypt_info(card_number, encryption_key)

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
        audit.log("Saving the credit card info")
        return redirect("list_cards", product_id=product_id)
    else:
        return render(request, "payment/add_new_card.html", {"product_id": product_id})


def list_cards(request, product_id):
    audit.log(f"Listing the credit card for user {request.user.id}")
    product = Product.objects.filter(id=product_id)[0]
    qrcode = Qrcode_info.objects.filter(id=product_id)[0]

    user_cards = CreditCard.objects.filter(user_id=request.user.id)

    return render(
        request,
        "payment/card_list.html",
        {"cards": user_cards, "product": product},
    )


def check_emerago(ip_addr):
    audit.log(f"Emberago checking for the IP {ip_addr}")
    sanction_msg = ""

    try:
        embargo_response = embargo.ip_check(ip=ip_addr)
        print(f"Response: {embargo_response.result}")
        audit.log(f"A user with ip addresss {ip_addr} has tried to login")
        sanctions_count= embargo_response.result.count
        sanctions_count = 0
        if sanctions_count >= 1:
            sanction_msg=embargo_response.result.summary
            audit.log(f"Sanction_msg is ", sanction_msg)
        return sanctions_count
        return sanctions_count
    except pe.PangeaAPIException as err:
        print(f"Embargo Request Error: {err.response.summary}")
        for er in err.errors:
            print(f"\t{er.detail} \n")


def ip_intel(ip_addr):
    try:
        audit.log(f"IP intel checking for the IP {ip_addr}")
        intel = IpIntel(token, config=config)
        response = intel.get_domain(
            ip=ip_addr, provider="digitalelement", verbose=True, raw=True
        )

        if response.result.data.domain_found:
            audit.log("IP domain was found")
            return True
        else:
            audit.log("IP domain was not found")
            return False

    except pe.PangeaAPIException as e:
        print(e)


def check_password(request):
    if request.POST:
        print("possting 1232", request.POST)
        encryption_key = request.POST["encryption_key"]

        return redirect(
            "success",
        )

    return render(request, "payment/password.html")

def succesfull(request):
    ip_addr = get_public_ip()
    emerago = check_emerago(ip_addr)
    ipintel = ip_intel(ip_addr)

    if emerago == 0 and ipintel:
        audit.log(f"Checks were succesfull")
        return render(request, "succesfull.html")
    else:
        audit.log(f"Checks had failed. Redirecting to malicious_data.html")
        return render(request, "malicious_data.html")

