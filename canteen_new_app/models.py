from django.db import models
class Order(models.Model):
   o_id=models.CharField(max_length=15,default=False)
   total_amt=models.IntegerField(default=False)
   ordered_items=models.CharField(max_length=30,default=False)
   #mobileno=models.IntegerField()
    
class Payment(models.Model):
    o_id=models.CharField(max_length=15,default=False)
    total_amt=models.IntegerField(default=False)
    #mobileno=models.IntegerField()

class Product(models.Model):
    p_id=models.CharField(max_length=15,default=False)
    category=models.CharField(max_length=15,default=False)
    product_name=models.CharField(max_length=30,default=False)
    availability=models.CharField(max_length=10,default=False)
    price=models.IntegerField(default=False)
    link=models.CharField(max_length=1000,default=False)
    quantity=models.IntegerField(default=False)

class Stock(models.Model):
    s_id=models.CharField(max_length=15,default=False)
    quantity_available=models.CharField(max_length=10,default=False)
    item_name=models.CharField(max_length=25,default=False)    

class Carttable(models.Model):
    user_id=models.IntegerField(default=False)
    product_name=models.CharField(max_length=25,default=False)
    quantity=models.IntegerField(default=False)
    price=models.IntegerField(default=False)
# Create your models here.
