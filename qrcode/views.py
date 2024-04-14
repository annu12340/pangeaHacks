from django.shortcuts import render
from .models import Qrcode_info


def qrcode(request):
    if request.POST:
        print("********************************")
        parent = request.POST['parent']
        childname = request.POST['childname']

        relationship = request.POST['relationship']
        streetaddress = request.POST['streetaddress']
        phone = request.POST['phone']
        towncity = request.POST['towncity']
        postcode = request.POST['postcode']
        form = Qrcode_info(parent=parent, childname=childname,  relationship=relationship, streetaddress=streetaddress,
                           towncity=towncity, postcode=postcode, phone=phone)
        form.save()

        asset_name = '-'.join(childname.split(" "))
        description = "This assest is created for"+asset_name
        intent = "http://127.0.0.1:8000/qrcode/"+str(form.id)
        parent_name = parent.split(" ")
    
        return render(request, 'checkout.html', {'img_url': "https://www.qrcode-monkey.com/img/default-preview-qr.svg"})

 
    return render(request, 'qrcode/qrcode_generation.html')


def qrcode_detail(request, qrcode_id):
    qrcode_details = Qrcode_info.objects.get(id=qrcode_id)
    scanid = request.GET.get('scanId', '')
    print(scanid)
    context = {'qrcode_details': qrcode_details, }
    return render(request, 'qrcode/qrcode_details.html', context)
