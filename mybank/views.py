from django.contrib import messages
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from . import forms
from . import models
from mybank.models import Transfers, Customers
import random

my_sender = ""
my_receiver = ""

account_number = 10000

# def randomGen():
#     # return a 6 digit random number
#     return int(random.uniform(1000000, 9999999))


def index(request):
    return render(request, "index.html")


def send_customers(request):
    cust = Customers.objects.all()
    return render(request, "send_customer_list.html", {"customers": cust})


def user_accnt(request):
    try:
        global my_sender
        my_sender = request.POST.get("mysend")
        print(my_sender+'userdetails')
        curr_user = Customers.objects.get(user_name=my_sender)  # getting details of current user
    except:
        # if no details exist (new user), create new details
        curr_user = Customers()
        # curr_user.account_number = randomGen()  # random account number for every new user
        global account_number
        curr_user.account_number = account_number
        account_number += 1
        curr_user.balance = 0
        curr_user.user_name = request.user
        curr_user.save()
    return render(request, "profile.html", {"curr_user": curr_user})


def receive_customers(request):
    print(my_sender+'excluded')
    cust = Customers.objects.exclude(user_name=my_sender)
    return render(request, "receive_customer_list.html", {"customers": cust})



def money_transfer(request):
    if request.method == "POST":
        global my_receiver
        my_receiver = request.POST.get("myreceive")
        print(my_receiver)
        # form = forms.MoneyTransferForm(request.POST)
        # print(request.POST.get("amount"))
        # print(form.is_valid())
        # if form.is_valid():
        #     form.save()

        curr_user = models.Customers.objects.get(user_name=my_sender)
        # print(curr_user.balance)
        temp = curr_user  # NOTE: Delete this instance once money transfer is done

        dest_user = models.Customers.objects.get(user_name=my_receiver)

        # curr_accnt = curr_user.account_number

        print('form valid')
        # transfer_amount = models.Transfers.objects.get(account_number=curr_accnt).enter_the_amount_to_be_transferred_in_INR  # FIELD 2
        transfer_amount = int(request.POST.get("amount"))


        # print(type(transfer_amount))
        if curr_user.balance > transfer_amount:
            curr_user.balance = curr_user.balance - transfer_amount
            dest_user.balance = dest_user.balance + transfer_amount
        else:
            print("insufficient balance!")
            messages.error(request, "Insufficient Balance!!")
            return render(request, "index.html")

            # Save the changes before redirecting
        models.Transfers.objects.create(account_number_id=curr_user.account_number,
                                        enter_the_amount_to_be_transferred_in_INR=transfer_amount)
        curr_user.save()
        dest_user.save()

        # temp.delete()  # NOTE: Now deleting the instance for future money transactions

        return render(request, "thanks.html")
    else:
        form = forms.MoneyTransferForm()
    messages.error(request, "Money transfer not Successful!")
    return render(request, "index.html")
