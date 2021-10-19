from django.db import models
import datetime


class Customers (models.Model):
    # (Name, Sex, DOB, Annual income, Email, Mobile number, Occupation)
    objects = None
    account_number = models.IntegerField(primary_key=True, null=False, default=None)
    # account_number = models.IntegerField(default = None)
    name = models.CharField(max_length = 50, default = None)
    sex = models.CharField(max_length = 1, default = None)
    email = models.EmailField(default = None)
    mobile = models.IntegerField(default = 0)
    user_name = models.CharField(max_length = 150, default = None)
    balance = models.IntegerField(default=0)


class Transfers(models.Model):
    objects = None
    account_number = models.ForeignKey(Customers, on_delete=models.CASCADE)
    # enter_the_destination_account_number = models.IntegerField()
    enter_the_amount_to_be_transferred_in_INR = models.IntegerField()