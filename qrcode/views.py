import os, time
from pathlib import Path
from django.shortcuts import render, redirect
import segno
import webbrowser

from .models import Qrcode_info
from utils.ip_address import get_public_ip
from utils.location_marker import mark_location
from utils.twilio import send_twilio_msg
from utils.pplx import convert_to_regional_language
from utils.calculate_sha256 import calculate_sha256
from dotenv import load_dotenv
from backend import settings

import pangea.exceptions as pe
from pangea.config import PangeaConfig
from pangea.services import FileScan, FileIntel, IpIntel, Redact, UrlIntel, Audit
from pangea.tools import logger_set_pangea_config

load_dotenv()
token = os.getenv("PANGEA_TOKEN")
domain = os.getenv("PANGEA_DOMAIN")

config = PangeaConfig(domain=domain, queued_retry_enabled=False)
client = FileScan(token, config=config, logger_name="pangea")
intel = UrlIntel(token, config=config)
audit = Audit(os.getenv("PANGEA_TOKEN"), config=config)

def file_scan(file_name):
    audit.log(f"Performing file scan on the file {file_name}")
    BASE_DIR = Path(__file__).resolve().parent
    file_path = str(BASE_DIR / "media" / "reports" / file_name)

    exception = None
    try:
        with open(file_path, "rb") as f:
            response = client.file_scan(file=f, verbose=True)

        audit.log("Scan success on first attempt...")
        audit.log(f"Response: {response.summary}")
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
        audit.log("Got result successfully...")
        audit.log(f"Response: {response.result}")
    except pe.PangeaAPIException as e:
        print(f"Request Error: {e.response.summary}")
        for err in e.errors:
            print(f"\t{err.detail} \n")


def file_intel(file_name):
    try:
        audit.log(f"Getting Hash for the file")
        indicator = calculate_sha256(file_name)
        audit.log(f"Performing file intel on the file {file_name}")
        response = intel.hash_reputation(
            hash=indicator,
            hash_type="sha256",
            provider="reversinglabs",
            verbose=True,
            raw=True,
        )
        print("Result:")
        print(response.result.data)
        return response.result.data.score
    except pe.PangeaAPIException as e:
        print(e)


def url_intel(url):
    try:
        audit.log(f"Performing url intel on the file {url}")
        url_list = [url]
        response = intel.reputation_bulk(
            urls=url_list, provider="crowdstrike", verbose=True, raw=True
        )
        print("Result:", response)
        score = response.result.data[url_list[0]].score
        if score == 0:
            return True
        elif score == 100:
            return False
    except pe.PangeaAPIException as e:
        print(e)


def qrcode(request, product_id):
    if request.POST:
        print("********************************")
        parent = request.POST["parent"]
        childname = request.POST["childname"]

        relationship = request.POST["relationship"]
        streetaddress = request.POST["streetaddress"]
        phone = request.POST["phone"]
        towncity = request.POST["towncity"]
        postcode = request.POST["postcode"]
        postcode = request.POST["postcode"]
        redact_data = request.POST["redact_data"]
        notify = request.POST["notify"]
        url = request.POST["url"]

        file = request.FILES.get("fileInput")
        qrcode_info = Qrcode_info(
            parent=parent,
            childname=childname,
            relationship=relationship,
            streetaddress=streetaddress,
            towncity=towncity,
            postcode=postcode,
            phone=phone,
            photo=file,
            details_url=url,
            redact_data=redact_data,
            notify=notify,
            created_by=request.user.id,
        )
        qrcode_info.save()

        # ----Verification -----
        data_valid = True
        if url_intel(url) == False:
            data_valid = False


        if file and file_intel(file)!=0:
            if file_scan(file)==100:
                data_valid=False

        if data_valid==False:
            audit.log(f"Data is malicious. Redirecting to malicious_data.html")
            return render(request, "malicious_data.html")

        # Save the model instance
        file_scan(file)

        # Generating the QR Code
        audit.log("Generating the new QR Code")
        qrcode_data = "http://127.0.0.1:8000/qrcode/" + str(qrcode_info.id)
        qrcode = segno.make_qr(qrcode_data)
        qrcode_path = f"{settings.MEDIA_ROOT}/qrcode/{qrcode_info.id}.png"
        qrcode.save(
            f"{qrcode_path}",
            scale=5,
            dark="brown",
            data_dark="orange",
        )
        webbrowser.open(qrcode_path)

        return redirect("checkout", product_id=product_id)

    return render(request, "qrcode/qrcode_generation.html")


def redact_info(text):
    audit.log(f"Redacting PII from: {text}")
    try:
        redact = Redact(token, config=config)
        redact_response = redact.redact(text=text)
        print(f"Redacted text: {redact_response.result.redacted_text}")
        return redact_response.result.redacted_text
    except pe.PangeaAPIException as e:
        print(f"Redact Request Error: {e.response.summary}")
        for err in e.errors:
            print(f"\t{err.detail} \n")


def qrcode_detail(request, qrcode_id):
    qrcode_details = Qrcode_info.objects.get(id=qrcode_id)
    region=''
    try:
        ip = get_public_ip()

        intel = IpIntel(token, config=config)
        audit.log("Getting the coordinates of the ip scan")
        response = intel.geolocate_bulk(ips=[ip])
        print(f"Response: {response.result}")
        latitude=response.result.data.get(ip).latitude
        longitude=response.result.data.get(ip).longitude
        # region=response.result.data.get(ip).region

        mark_location(latitude,longitude)
        message = f"""
            Your child was found at this location.
            \nLatitude: {latitude}, Longitude: {longitude}, Region: {region}
        """
        regional_language = ""
        regional_language=convert_to_regional_language(region, message)
        send_twilio_msg(qrcode_details.phone, message)

    except pe.PangeaAPIException as e:
        print(f"Request Error: {e.response.summary}")
        for err in e.errors:
            print(f"\t{err.detail} \n")

    description = f"""
    <p><strong>This is {qrcode_details.childname}, {qrcode_details.relationship} of {qrcode_details.parent}. The child has been reported missing.</strong></p>
    <p>If found, please contact {qrcode_details.phone}</p>
    <br>
    <br>
    <p><strong>Address</strong></p>
    <hr>
    <p>{qrcode_details.streetaddress}<br>
    {qrcode_details.towncity}<br>
    {qrcode_details.postcode}</p>
"""
    if qrcode_details.redact_data == 'yes':
        description = redact_info(description)

    context = {
        "description": description,
        "regional_language": regional_language,
    }
    return render(request, "qrcode/qrcode_details.html", context)


def view_map(request):
    return render(request, "map.html")
