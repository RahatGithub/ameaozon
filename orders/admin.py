from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']
    inlines = [CartItemInline]

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['tracking_number', 'user', 'status', 'payment_method', 'payment_completed', 'total_price', 'created_at']
    list_filter = ['status', 'payment_method', 'payment_completed']
    search_fields = ['tracking_number', 'user__username', 'email', 'phone']
    inlines = [OrderItemInline]

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)