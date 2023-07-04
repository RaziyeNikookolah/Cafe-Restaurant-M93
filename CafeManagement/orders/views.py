from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import CartForm, BookTableForm
from home.models import RestaurantInfo
from .models import Order_menuItem, Order, Table
from menu_items.models import MenuItem
import json


def cart(request):
    try:
        order_items = json.loads(request.COOKIES["cart"])
        menuItems=[(MenuItem.objects.get(id=i),j["quantity"]) for i,j in order_items.items()]
        total_price=0
        for menu_item in menuItems:
            total_price+=menu_item[0].price*menu_item[1]
    except:
        menuItems=()
        total_price=0

    if request.method == "POST" and menuItems:
        form=CartForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if data['table_number']:
                table=Table.objects.get(number=data['table_number'])
            else:
                table=None
            order = Order.objects.create(table=table, phone_number=data['phone_number'])
            for menuItem in menuItems:
                Order_menuItem.objects.create(
                    menuItem=menuItem[0], order=order, quantity=menuItem[1]
                )
        response = HttpResponseRedirect(reverse("home"))
        response.delete_cookie("cart")
        return response
    else:
        form=CartForm()
    info = RestaurantInfo.objects.first()
    return render(request, "cart.html", context={"info": info, "form":form, "menuItems": menuItems, "total_price":total_price})


def book(request):
    info = RestaurantInfo.objects.first()
    if request.method == "POST":
        form = BookTableForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            print(data)
            return redirect("home")

    else:
        form = BookTableForm()
    return render(request, "book.html", context={"form": form, "info": info})
