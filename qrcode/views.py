import os, time
from pathlib import Path
from django.shortcuts import render, redirect
import segno

from .models import Qrcode_info
from utils.ip_address import get_public_ip 
from utils.location_marker import mark_location
from dotenv import load_dotenv
from backend import settings

import pangea.exceptions as pe
from pangea.config import PangeaConfig
from pangea.services import FileScan, FileIntel, IpIntel
from pangea.tools import logger_set_pangea_config

load_dotenv()
token = os.getenv("PANGEA_TOKEN")
domain = os.getenv("PANGEA_DOMAIN")

config = PangeaConfig(domain=domain, queued_retry_enabled=False)
client = FileScan(token, config=config, logger_name="pangea")

def file_scan(file_name):
    print("Checking file...")
    # TODO: Fix this
    BASE_DIR = Path(__file__).resolve().parent
    file_path = str(BASE_DIR / "media" / "reports" / file_name)  
    print("file_path",file_path)
    exception = None
    try:
        with open(file_path, "rb") as f:
            response = client.file_scan(file=f, verbose=True)

        print("Scan success on first attempt...")
        print(f"Response: {response.result}")
        exit()
    except pe.AcceptedRequestException as e:
        # Save the exception value to request the results later.
        exception = e
        print("This is a expected exception")
        print(f"Request Error: {e.response.summary}")
        for err in e.errors:
            print(f"\t{err.detail} \n")
    except pe.PangeaAPIException as e:
        print("This is a unexpected exception")
        print(f"Request Error: {e.response.summary}")
        for err in e.errors:
            print(f"\t{err.detail} \n")
        return

    print("We are going to sleep some time before we poll result...")
    # Wait a set amount of time for the results to be ready and then poll for the results.
    time.sleep(20)

    try:
        # poll for the results
        response = client.poll_result(exception)
        print("Got result successfully...")
        print(f"Response: {response.result}")
    except pe.PangeaAPIException as e:
        print(f"Request Error: {e.response.summary}")
        for err in e.errors:
            print(f"\t{err.detail} \n")

def file_intel(file_name):
    pass

def qrcode(request,product_id):
    if request.POST:
        print("********************************")
        parent = request.POST['parent']
        childname = request.POST['childname']

        relationship = request.POST['relationship']
        streetaddress = request.POST['streetaddress']
        phone = request.POST['phone']
        towncity = request.POST['towncity']
        postcode = request.POST['postcode']
     
        file=request.FILES.get('fileInput')
        qrcode_info = Qrcode_info(
            parent=parent,
            childname=childname,
            relationship=relationship,
            streetaddress=streetaddress,
            towncity=towncity,
            postcode=postcode,
            phone=phone,
            reports=file
      
         
            # created_by= request.user.id #TODO: Need to update
        )
        
    
        # Save the model instance
        qrcode_info.save()
        # file_scan(file)
   
        # Generating the QR Code
        qrcode_data = "http://127.0.0.1:8000/qrcode/"+str(qrcode_info.id)
        qrcode = segno.make_qr(qrcode_data)
        qrcode.save(
            f"{settings.MEDIA_ROOT}/qrcode/{qrcode_info.id}.png",
            scale=5,
            dark="blue",
            data_dark="darkblue",
        )
    
        return redirect('checkout', product_id=product_id)

 
    return render(request, 'qrcode/qrcode_generation.html')


def qrcode_detail(request, qrcode_id):
    qrcode_details = Qrcode_info.objects.get(id=qrcode_id)
   
    try:
        ip=get_public_ip()

        intel = IpIntel(token, config=config)
        response = intel.geolocate_bulk(ips=[ip])
        print(f"Response: {response.result}")
        latitude=response.result.data.get(ip).latitude
        longitude=response.result.data.get(ip).longitude
        mark_location(latitude,longitude)


    except pe.PangeaAPIException as e:
        print(f"Request Error: {e.response.summary}")
        for err in e.errors:
            print(f"\t{err.detail} \n")


    context = {'qrcode_details': qrcode_details, }
    return render(request, 'qrcode/qrcode_details.html', context)

def view_map(request):
    return render(request, 'map.html')