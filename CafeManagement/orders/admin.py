from django.contrib import admin
from .models import Order, Receipt, Table, Order_menuItem


class TableAdmin(admin.ModelAdmin):
    fields = ('number', 'space_position', 'capacity')
    list_display = ('number', 'capacity', 'space_position')
    search_fields = ('number',)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('table', 'serving_status',)
    search_fields = ('order', 'phone_number', 'serving_status')


class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('order', 'total_price', 'final_price')
    search_fields = ('order',)


class Order_menuItemAdmin(admin.ModelAdmin):
    list_display = ('menuItem', 'quantity')
    search_fields = ('menuItem',)


admin.site.register(Table, TableAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Receipt, ReceiptAdmin)
admin.site.register(Order_menuItem, Order_menuItemAdmin)
