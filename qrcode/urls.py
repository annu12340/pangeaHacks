from django.urls import path
from . import views


urlpatterns = [

    path('generate/<product_id>', views.qrcode, name='qrcode'),
    path('map/', views.view_map, name='view_map'),
    
    path('<qrcode_id>', views.qrcode_detail, name='qrcode-details'),
]
