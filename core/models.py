from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

class User(AbstractUser):
    pass




class CafeworkingHoure(models.Model):
    Day_choise =(
        (0 , "saturday"),
        (1 ,"sunday"), 
        (2 ,"monday"), 
        (3 ,"Tuseday"),
        (4 ,"wednesdy"),
        (5 ,"Thursdday"),
        (6 ,"Friday")
    )

    day_of_week = models.IntegerField(choices= Day_choise)
    start_time = models.TimeField()
    End_time = models.TimeField()

    def __str__(self):
        return f"{self.day_of_week} : {self.start_time} - {self.End_time}"

class CafeTable(models.Model):
    table_number = models.PositiveSmallIntegerField(unique=True)
    capacity = models.PositiveBigIntegerField()
    price_oer_person = models.DecimalField(max_digits= 100 , decimal_places= 3)
    time_slot_minuts = models.PositiveBigIntegerField()

    working_hour = models.ForeignKey(CafeworkingHoure , on_delete=models.CASCADE ,related_name="tables")
    

    def Calculate_the_table(self):
        return self.capacity * self.price_oer_person
    def __str__(self):
        return f"Table {self.table_number} , {self.capacity}"
    
class Category(models.Model):
    name = models.CharField
    def __str__(self):
        return self.name
    

class FOOd_ITem(models.Model):
    name = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=100 ,decimal_places=3 )
    category = models.ForeignKey(Category , on_delete= models.CASCADE)
    is_available = models.BooleanField(default=True)

    def get_final_price(self):
        final_price = self.price
        item_discount = Discount.object.filter(type ="item" ,food_item = self).first

        if item_discount :
            return final_price -(final_price * item_discount/ 100)
        category_discount = Discount.object.filter(type="item" , category = self.category).first
        if category_discount : 
            return final_price (final_price * category_discount / 100)
        
        return final_price 
    def __str__(self):
        return self.name
    
class Discount(models.Model):
    Discount_TYPE = (
        ("item" , "Item"),
        ("caregory" , "Category"),
    )

    name = models.CharField(max_length=100)
    percentage = models.PositiveIntegerField()
    type = models.CharField(max_length=10 , choices=Discount_TYPE)

    food_item = models.ForeignKey(
        FOOd_ITem,on_delete=models.CASCADE , null=True , blank=True
    )
    category = models.ForeignKey(
        Category , on_delete=models.CASCADE ,null=True ,blank=True
    )
    def clean(self):
        if self.type =="item" and not self.food_item:
            raise ValidationError("Item discount  must have in the category ")
        if self.type == "category" and not self.category:
            raise ValidationError("the item should have the must category")
    def __str__(self):
        return f"{self.name} % {self.percentage}"

from django.conf import settings

class Reservation(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
