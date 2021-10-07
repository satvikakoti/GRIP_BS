from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from . import forms
from . import models
from mybank.models import Status
import random


def randomGen():
    # return a 6 digit random number
    return int(random.uniform(1000000, 9999999))


def index(request):
    return render(request, "index.html")


def user_accnt(request):
    try:
        curr_user = Status.objects.get(user_name=request.user)  # getting details of current user
    except:
        # if no details exist (new user), create new details
        curr_user = Status()
        curr_user.account_number = randomGen()  # random account number for every new user
        curr_user.balance = 0
        curr_user.user_name = request.user
        curr_user.save()
    return render(request, "profile.html", {"curr_user": curr_user})


def money_transfer(request):
    if request.method == "POST":
        form = forms.MoneyTransferForm(request.POST)
        if form.is_valid():
            form.save()

            curr_user = models.MoneyTransfer.objects.get(enter_your_user_name=request.user)
            dest_user_acc_num = curr_user.enter_the_destination_account_number

            temp = curr_user  # NOTE: Delete this instance once money transfer is done

            dest_user = models.Status.objects.get(account_number=dest_user_acc_num)  # FIELD 1
            transfer_amount = curr_user.enter_the_amount_to_be_transferred_in_INR  # FIELD 2
            curr_user = models.Status.objects.get(user_name=request.user)  # FIELD 3

            # Now transfer the money!
            curr_user.balance = curr_user.balance - transfer_amount
            dest_user.balance = dest_user.balance + transfer_amount

            # Save the changes before redirecting
            curr_user.save()
            dest_user.save()

            temp.delete()  # NOTE: Now deleting the instance for future money transactions

        return redirect("profile.html")
    else:
        form = forms.MoneyTransferForm()
    return render(request, "money_transfer.html", {"form": form})