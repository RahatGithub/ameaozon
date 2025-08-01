from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.category_add, name='category_add'),
    path('categories/edit/<int:category_id>/', views.category_edit, name='category_edit'),
    path('subcategories/', views.subcategory_list, name='subcategory_list'),
    path('subcategories/add/', views.subcategory_add, name='subcategory_add'),
    path('subcategories/edit/<int:subcategory_id>/', views.subcategory_edit, name='subcategory_edit'),
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.product_add, name='product_add'),
    path('products/edit/<int:product_id>/', views.product_edit, name='product_edit'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/<str:tracking_number>/', views.order_detail, name='order_detail'),
    path('orders/update-status/<str:tracking_number>/', views.update_order_status, name='update_order_status'),
    path('carousel/', views.carousel_list, name='carousel_list'),
    path('carousel/add/', views.carousel_add, name='carousel_add'),
    path('carousel/edit/<int:image_id>/', views.carousel_edit, name='carousel_edit'),
    path('carousel/toggle-active/<int:image_id>/', views.carousel_toggle_active, name='carousel_toggle_active'),
    path('carousel/delete/<int:image_id>/', views.carousel_delete, name='carousel_delete')
]