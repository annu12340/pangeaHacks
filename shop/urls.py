from django.urls import path
from . import views


urlpatterns = [
    path("", views.shop_page, name="shop"),
    path("product/<product_id>", views.product_details, name="product-details"),
    # Card details url
    path("checkout/<product_id>", views.checkout, name="checkout"),
    path("new_card/<product_id>", views.new_card, name="new_card"),
    path("list_cards/<product_id>", views.list_cards, name="list_cards"),
    path("payment/password/<str:redirect_type>", views.check_password, name="password"),
    path("payment/success/<product_id>", views.succesfull, name="success"),
]
