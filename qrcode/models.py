from django.db import models


class Qrcode_info(models.Model):
    parent = models.CharField(max_length=40, default='')
    childname = models.CharField(max_length=30)
    relationship = models.CharField(max_length=50)
    streetaddress = models.CharField(max_length=50)
    towncity = models.CharField(max_length=50)
    postcode = models.CharField(max_length=50)
    phone = models.CharField(max_length=30)
    date = models.DateTimeField(auto_now_add=True)
    reports = models.FileField(blank=True, upload_to='reports')
    # redact_data=models.CharField(max_length=30)
    # notify=models.CharField(max_length=30)
    # created_by=models.IntegerField()

    def __str__(self):
        return self.parent
