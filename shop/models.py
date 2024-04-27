from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=30)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to="products")
    price = models.IntegerField()
    details = models.TextField()
    rating = models.CharField(max_length=10)
    count = models.IntegerField(default=452)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class CreditCard(models.Model):
    card_number = models.CharField(max_length=16)
    cardholder_name = models.CharField(max_length=100)
    expiry_date = models.CharField(max_length=7)
    security_number = models.CharField(max_length=3)
    user_id = models.IntegerField()
    encryption_key=models.CharField(max_length=30,default='')

    def __str__(self):
        return f"Credit Card: {self.card_number}"
