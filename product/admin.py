from django.contrib import admin
from .models import Category, Product, ShippingAddress, Order, OrderItem,Cart

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'price', 'stock_qty', 'created_at', 'updated_at')
    search_fields = ('title', 'category__name')
    list_filter = ('category', 'created_at')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'address_line1', 'city', 'state', 'pincode')
    search_fields = ('customer__name', 'city', 'state', 'pincode')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'customer', 'order_date', 'payment_status', 'order_status', 'order_amount')
    search_fields = ('order_id', 'customer__name')
    list_filter = ('payment_status', 'order_status', 'order_date')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity', 'unit_price')
    search_fields = ('order__order_id', 'product__title')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'quantity', 'customer')
 



 