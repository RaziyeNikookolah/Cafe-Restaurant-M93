from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import CartForm, BookTableForm
from home.models import RestaurantInfo
from .models import Order_menuItem, Order, Table, Receipt
from menu_items.models import MenuItem
from django.views import View
import json


class CartView(View):
    info = RestaurantInfo.objects.first()

    def get(self, request):
        (menuItems, total_price) = CartView.load_cookie(request)
        form = CartForm()
        return render(
            request,
            "cart.html",
            context={
                "info": CartView.info,
                "form": form,
                "menuItems": menuItems,
                "total_price": total_price,
            },
        )

    def post(self, request):
        menuItems, total_price = CartView.load_cookie(request)
        form = CartForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            table = Table.objects.get(number=data["table_number"])
            order = Order.objects.create(table=table, phone_number=data["phone_number"])
            reciept = Receipt.objects.create(
                order=order, total_price=total_price, final_price=total_price
            )
            for menuItem in menuItems:
                Order_menuItem.objects.create(
                    menuItem=menuItem[0], order=order, quantity=menuItem[1]
                )

            request.session["last_order"] = order.id
            if not request.session.get("orders_history"):
                request.session["orders_history"] = [order.id]
            else:
                request.session["orders_history"].append(order.id)

            response = HttpResponseRedirect(reverse("customer"))
            response.delete_cookie("cart")
            return response
        return render(
            request,
            "cart.html",
            context={
                "info": CartView.info,
                "form": form,
                "menuItems": menuItems,
                "total_price": total_price,
            },
        )

    @staticmethod
    def load_cookie(request):
        try:
            order_items = json.loads(request.COOKIES["cart"])
            menuItems = [
                (MenuItem.objects.get(id=i), j["quantity"])
                for i, j in order_items.items()
            ]
            total_price = 0
            for menu_item in menuItems:
                total_price += menu_item[0].price * menu_item[1]
        except:
            menuItems = ()
            total_price = 0
        return (menuItems, total_price)


class CustomerView(View):
    info = RestaurantInfo.objects.first()

    def get(self, request):
        orders_id = request.session.get("orders_history", [])
        orders = [Order.objects.get(id=order_id) for order_id in orders_id]
        return render(
            request,
            "customer.html",
            context={"orders": orders, "info": CustomerView.info},
        )


class BookView(View):
    info = RestaurantInfo.objects.first()

    def get(self, request):
        form = BookTableForm()
        return render(
            request, "book.html", context={"form": form, "info": CartView.info}
        )

    def post(self, request):
        form = BookTableForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            print(data)
            return redirect("home")
        return render(
            request, "book.html", context={"form": form, "info": CartView.info}
        )
