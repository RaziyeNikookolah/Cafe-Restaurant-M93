from django.shortcuts import render, redirect
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
    PermissionRequiredMixin,
)
from django.views import View
from orders.models import Order, Receipt
from menu_items.models import MenuItem
from django.http import Http404
from .forms import ChangeOrderStatusForm



class DashboardView(LoginRequiredMixin, UserPassesTestMixin, View):

    login_url = "/login/"

    def test_func(self):
        result = (
            self.request.user.groups.filter(name="cashier").exists()
            or self.request.user.groups.filter(name="manager").exists()
        )
        if not result:
            raise Http404
        return result

    def get(self, request):
        all_orders = Order.objects.all()
        recent_orders=all_orders[:10]
        pending_orders=all_orders.filter(serving_status=1)
        confirmed_orders=all_orders.filter(serving_status=2)
        cooking_orders=all_orders.filter(serving_status=3)
        served_orders=all_orders.filter(serving_status=4)
        canceled_orders=all_orders.filter(serving_status=5)
        orders= {"all_orders": all_orders,"recent_orders":recent_orders,"pending_orders":pending_orders,"confirmed_orders":confirmed_orders,"cooking_orders":cooking_orders,"served_orders":served_orders, "canceled_orders":canceled_orders}
        menuItems = MenuItem.objects.all()
        reciepts = Receipt.objects.all()
        order_status_form = ChangeOrderStatusForm()
        return render(
            request,
            "dashboard/index.html",
            context={"orders": orders, "menuItems": menuItems, "reciepts": reciepts},
        )

    def post(self, request):
        if request.POST.get("serving_status"):
            print(request.POST)
            id=request.POST.get("order_id")
            new_status = request.POST.get("serving_status")
            Order.objects.filter(id=id).update(serving_status=new_status)
        return redirect('dashboard')

# class ManagerView(LoginRequiredMixin, PermissionRequiredMixin, View):

#     login_url = '/login/'
#     redirect_field_name = 'redirect_to'

#     def dispatch(self, *args, **kwargs):
#         if not self.request.user.is_authenticated:
#             return redirect(self.login_url)
#         elif not (
#             self.request.user.groups.filter(name="manager").exists()
#         ):
#             raise Http404
#         return super(ManagerView, self).dispatch(*args, **kwargs)

#     def get(self, request):
#         reciepts = Receipt.objects.all()
#         return render(request, 'manager.html', context={"reciepts":reciepts})
