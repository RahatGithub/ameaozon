from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Avg
from django.contrib import messages
from .models import Category, SubCategory, Product, Review, Wishlist, CarouselImage
from .forms import ReviewForm, CarouselImageForm


def home(request):
    categories = Category.objects.filter(is_active=True)
    featured_products = Product.objects.filter(is_available=True)[:8]
    carousel_images = CarouselImage.objects.all().order_by('order', '-created_at')
    
    context = {
        'categories': categories,
        'featured_products': featured_products,
        'carousel_images' : carousel_images,
    }
    return render(request, 'store/home.html', context)

def category_detail(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug, is_active=True)
    subcategories = category.subcategories.filter(is_active=True)
    
    # Get all products from all subcategories of this category
    products = Product.objects.filter(subcategory__category=category, is_available=True)
    
    context = {
        'category': category,
        'subcategories': subcategories,
        'products': products,
    }
    return render(request, 'store/category_detail.html', context)

def subcategory_detail(request, category_slug, subcategory_slug):
    category = get_object_or_404(Category, slug=category_slug, is_active=True)
    subcategory = get_object_or_404(SubCategory, slug=subcategory_slug, category=category, is_active=True)
    products = Product.objects.filter(subcategory=subcategory, is_available=True)
    
    context = {
        'category': category,
        'subcategory': subcategory,
        'products': products,
    }
    return render(request, 'store/subcategory_detail.html', context)

def product_detail(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug, is_available=True)
    related_products = Product.objects.filter(subcategory=product.subcategory).exclude(id=product.id)[:4]
    
    # Get reviews with comments
    reviews = product.reviews.exclude(comment='').order_by('-created_at')
    avg_rating = product.get_average_rating()
    
    # Review form
    if request.method == 'POST' and request.user.is_authenticated:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, 'Your review has been submitted!')
            return redirect('store:product_detail', product_slug=product.slug)
    else:
        form = ReviewForm()
    
    # Check if product is in user's wishlist
    in_wishlist = False
    if request.user.is_authenticated:
        wishlist = Wishlist.objects.filter(user=request.user).first()
        if wishlist and product in wishlist.products.all():
            in_wishlist = True
    
    context = {
        'product': product,
        'related_products': related_products,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'review_form': form,
        'in_wishlist': in_wishlist,
    }
    return render(request, 'store/product_detail.html', context)

def search(request):
    query = request.GET.get('q', '')
    products = []
    
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(subcategory__name__icontains=query) |
            Q(subcategory__category__name__icontains=query)
        ).filter(is_available=True).distinct()
    
    context = {
        'products': products,
        'query': query
    }
    return render(request, 'store/search_results.html', context)

@login_required
def wishlist(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    products = wishlist.products.all()
    
    context = {
        'wishlist': wishlist,
        'products': products
    }
    return render(request, 'store/wishlist.html', context)

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    
    if product not in wishlist.products.all():
        wishlist.products.add(product)
        messages.success(request, f'{product.name} added to your wishlist.')
    
    return redirect(request.META.get('HTTP_REFERER', 'store:home'))

@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist = Wishlist.objects.filter(user=request.user).first()
    
    if wishlist and product in wishlist.products.all():
        wishlist.products.remove(product)
        messages.success(request, f'{product.name} removed from your wishlist.')
    
    return redirect(request.META.get('HTTP_REFERER', 'store:wishlist'))