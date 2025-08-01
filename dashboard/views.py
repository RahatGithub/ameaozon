from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count
from django.utils.text import slugify
from accounts.models import User
from store.models import Category, SubCategory, Product, ProductImage, Review, CarouselImage
from orders.models import Order, OrderItem
from .forms import CategoryForm, SubCategoryForm, ProductForm, ProductImageFormSet
from store.forms import CarouselImageForm 
from .decorators import admin_required


@login_required
@admin_required
def admin_dashboard(request):
    # Get stats for dashboard
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='pending').count()
    completed_orders = Order.objects.filter(status='delivered').count()
    total_customers = User.objects.filter(user_type=User.CUSTOMER).count()
    total_products = Product.objects.count()
    total_revenue = Order.objects.filter(payment_completed=True).aggregate(Sum('total_price'))['total_price__sum'] or 0
    
    # Get recent orders
    recent_orders = Order.objects.all().order_by('-created_at')[:5]
    
    # Get popular products (most ordered)
    popular_products = Product.objects.annotate(
        order_count=Count('orderitem')
    ).order_by('-order_count')[:5]
    
    context = {
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'completed_orders': completed_orders,
        'total_customers': total_customers,
        'total_products': total_products,
        'total_revenue': total_revenue,
        'recent_orders': recent_orders,
        'popular_products': popular_products,
    }
    return render(request, 'dashboard/admin_dashboard.html', context)

@login_required
@admin_required
def category_list(request):
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'dashboard/category_list.html', context)

@login_required
@admin_required
def category_add(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save(commit=False)
            category.slug = slugify(category.name)
            category.save()
            messages.success(request, f'Category "{category.name}" added successfully.')
            return redirect('dashboard:category_list')
    else:
        form = CategoryForm()
    
    context = {
        'form': form,
        'title': 'Add Category'
    }
    return render(request, 'dashboard/category_form.html', context)

@login_required
@admin_required
def category_edit(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            category = form.save(commit=False)
            category.slug = slugify(category.name)
            category.save()
            messages.success(request, f'Category "{category.name}" updated successfully.')
            return redirect('dashboard:category_list')
    else:
        form = CategoryForm(instance=category)
    
    context = {
        'form': form,
        'title': 'Edit Category',
        'category': category
    }
    return render(request, 'dashboard/category_form.html', context)

@login_required
@admin_required
def subcategory_list(request):
    subcategories = SubCategory.objects.all()
    context = {
        'subcategories': subcategories
    }
    return render(request, 'dashboard/subcategory_list.html', context)

@login_required
@admin_required
def subcategory_add(request):
    if request.method == 'POST':
        form = SubCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            subcategory = form.save(commit=False)
            subcategory.slug = slugify(subcategory.name)
            subcategory.save()
            messages.success(request, f'SubCategory "{subcategory.name}" added successfully.')
            return redirect('dashboard:subcategory_list')
    else:
        form = SubCategoryForm()
    
    context = {
        'form': form,
        'title': 'Add SubCategory'
    }
    return render(request, 'dashboard/subcategory_form.html', context)

@login_required
@admin_required
def subcategory_edit(request, subcategory_id):
    subcategory = get_object_or_404(SubCategory, id=subcategory_id)
    
    if request.method == 'POST':
        form = SubCategoryForm(request.POST, request.FILES, instance=subcategory)
        if form.is_valid():
            subcategory = form.save(commit=False)
            subcategory.slug = slugify(subcategory.name)
            subcategory.save()
            messages.success(request, f'SubCategory "{subcategory.name}" updated successfully.')
            return redirect('dashboard:subcategory_list')
    else:
        form = SubCategoryForm(instance=subcategory)
    
    context = {
        'form': form,
        'title': 'Edit SubCategory',
        'subcategory': subcategory
    }
    return render(request, 'dashboard/subcategory_form.html', context)

@login_required
@admin_required
def product_list(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'dashboard/product_list.html', context)

@login_required
@admin_required
def product_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        formset = ProductImageFormSet(request.POST, request.FILES, prefix='images')
        
        if form.is_valid() and formset.is_valid():
            product = form.save(commit=False)
            product.slug = slugify(product.name)
            product.save()
            
            # Save product images
            instances = formset.save(commit=False)
            for instance in instances:
                instance.product = product
                instance.save()
            
            messages.success(request, f'Product "{product.name}" added successfully.')
            return redirect('dashboard:product_list')
    else:
        form = ProductForm()
        formset = ProductImageFormSet(prefix='images')
    
    context = {
        'form': form,
        'formset': formset,
        'title': 'Add Product'
    }
    return render(request, 'dashboard/product_form.html', context)

@login_required
@admin_required
def product_edit(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        formset = ProductImageFormSet(request.POST, request.FILES, prefix='images', instance=product)
        
        if form.is_valid() and formset.is_valid():
            product = form.save(commit=False)
            product.slug = slugify(product.name)
            product.save()
            
            # Save product images
            formset.save()
            
            messages.success(request, f'Product "{product.name}" updated successfully.')
            return redirect('dashboard:product_list')
    else:
        form = ProductForm(instance=product)
        formset = ProductImageFormSet(prefix='images', instance=product)
    
    context = {
        'form': form,
        'formset': formset,
        'title': 'Edit Product',
        'product': product
    }
    return render(request, 'dashboard/product_form.html', context)

@login_required
@admin_required
def order_list(request):
    orders = Order.objects.all().order_by('-created_at')
    context = {
        'orders': orders
    }
    return render(request, 'dashboard/order_list.html', context)

@login_required
@admin_required
def order_detail(request, tracking_number):
    order = get_object_or_404(Order, tracking_number=tracking_number)
    order_items = order.items.all()
    
    context = {
        'order': order,
        'order_items': order_items
    }
    return render(request, 'dashboard/order_detail.html', context)

@login_required
@admin_required
def update_order_status(request, tracking_number):
    order = get_object_or_404(Order, tracking_number=tracking_number)
    
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in dict(Order.STATUS_CHOICES).keys():
            order.status = status
            order.save()
            messages.success(request, f'Order status updated to "{dict(Order.STATUS_CHOICES)[status]}"')
        else:
            messages.error(request, 'Invalid status')
    
    return redirect('dashboard:order_detail', tracking_number=tracking_number)



# Carousel related views
@login_required
@admin_required
def carousel_list(request):
    carousel_images = CarouselImage.objects.all().order_by('order', '-created_at')
    context = {
        'carousel_images': carousel_images
    }
    return render(request, 'dashboard/carousel_list.html', context)

@login_required
@admin_required
def carousel_add(request):
    if request.method == 'POST':
        form = CarouselImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Carousel image added successfully.')
            return redirect('dashboard:carousel_list')
    else:
        form = CarouselImageForm()
    
    context = {
        'form': form,
        'title': 'Add Carousel Image'
    }
    return render(request, 'dashboard/carousel_form.html', context)

@login_required
@admin_required
def carousel_edit(request, image_id):
    carousel_image = get_object_or_404(CarouselImage, id=image_id)
    
    if request.method == 'POST':
        form = CarouselImageForm(request.POST, request.FILES, instance=carousel_image)
        if form.is_valid():
            form.save()
            messages.success(request, 'Carousel image updated successfully.')
            return redirect('dashboard:carousel_list')
    else:
        form = CarouselImageForm(instance=carousel_image)
    
    context = {
        'form': form,
        'carousel_image': carousel_image,
        'title': 'Edit Carousel Image'
    }
    return render(request, 'dashboard/carousel_form.html', context)

@login_required
@admin_required
def carousel_toggle_active(request, image_id):
    carousel_image = get_object_or_404(CarouselImage, id=image_id)
    carousel_image.is_active = not carousel_image.is_active
    carousel_image.save()
    
    status = "activated" if carousel_image.is_active else "deactivated"
    messages.success(request, f'Carousel image {status} successfully.')
    
    return redirect('dashboard:carousel_list')

@login_required
@admin_required
def carousel_delete(request, image_id):
    carousel_image = get_object_or_404(CarouselImage, id=image_id)
    
    if request.method == 'POST':
        carousel_image.delete()
        messages.success(request, 'Carousel image deleted successfully.')
        return redirect('dashboard:carousel_list')
    
    context = {
        'carousel_image': carousel_image
    }
    return render(request, 'dashboard/carousel_delete.html', context)