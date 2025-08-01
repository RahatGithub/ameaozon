from django.contrib import admin
from .models import Category, SubCategory, Product, ProductImage, CarouselImage, Review, Wishlist

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3

class CarouselImageAdmin(admin.ModelAdmin):
    list_display = ['order', 'is_active', 'created_at']
    list_editable = ['is_active', 'order']
    list_filter = ['is_active']

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', 'is_available', 'subcategory']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]

class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'is_active']
    prepopulated_fields = {'slug': ('name',)}

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(CarouselImage)
admin.site.register(Review)
admin.site.register(Wishlist)