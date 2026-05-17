from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.db.models import Q, Avg
from django.contrib import messages
from .models import Category, SubCategory, Product, Review, Wishlist, CarouselImage
from .forms import ReviewForm


def home(request):
    """Homepage with featured products and carousel."""
    categories = Category.objects.filter(is_active=True)
    featured_products = Product.objects.filter(is_available=True).order_by('-created_at')[:8]
    carousel_images = CarouselImage.objects.filter(is_active=True).order_by('order', '-created_at')

    context = {
        'categories': categories,
        'featured_products': featured_products,
        'carousel_images': carousel_images,
    }
    return render(request, 'store/home.html', context)

def category_detail(request, category_slug):
    """List all products within a category, paginated."""
    category = get_object_or_404(Category, slug=category_slug, is_active=True)
    subcategories = category.subcategories.filter(is_active=True)

    products_qs = Product.objects.filter(
        subcategory__category=category, is_available=True
    ).order_by('-created_at')
    paginator = Paginator(products_qs, 12)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'category': category,
        'subcategories': subcategories,
        'products': page_obj,
        'page_obj': page_obj,
        'page_param': 'page',
    }
    return render(request, 'store/category_detail.html', context)

def subcategory_detail(request, category_slug, subcategory_slug):
    """List all products within a subcategory, paginated."""
    category = get_object_or_404(Category, slug=category_slug, is_active=True)
    subcategory = get_object_or_404(SubCategory, slug=subcategory_slug, category=category, is_active=True)

    products_qs = Product.objects.filter(
        subcategory=subcategory, is_available=True
    ).order_by('-created_at')
    paginator = Paginator(products_qs, 12)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'category': category,
        'subcategory': subcategory,
        'products': page_obj,
        'page_obj': page_obj,
        'page_param': 'page',
    }
    return render(request, 'store/subcategory_detail.html', context)

def product_detail(request, product_slug):
    """Product page with images, reviews, rating, and add-to-cart/wishlist."""
    product = get_object_or_404(Product, slug=product_slug, is_available=True)
    related_products = Product.objects.filter(subcategory=product.subcategory).exclude(id=product.id)[:4]
    
    # Get reviews with comments
    reviews = product.reviews.exclude(comment='').order_by('-created_at')
    avg_rating = product.get_average_rating()
    
    # Review form
    if request.method == 'POST' and request.user.is_authenticated:
        form = ReviewForm(request.POST)
        if form.is_valid():
            _, created = Review.objects.update_or_create(
                product=product,
                user=request.user,
                defaults={
                    'rating': form.cleaned_data['rating'],
                    'comment': form.cleaned_data['comment'],
                }
            )
            if created:
                messages.success(request, 'Your review has been submitted!')
            else:
                messages.success(request, 'Your review has been updated!')
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
    """Search products by name, description, subcategory, or category."""
    query = request.GET.get('q', '')
    page_obj = None

    if query:
        products_qs = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(subcategory__name__icontains=query) |
            Q(subcategory__category__name__icontains=query)
        ).filter(is_available=True).distinct().order_by('-created_at')
        paginator = Paginator(products_qs, 12)
        page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'products': page_obj,
        'page_obj': page_obj,
        'page_param': 'page',
        'query': query,
    }
    return render(request, 'store/search_results.html', context)

@login_required
def wishlist(request):
    """Display the user's saved wishlist products."""
    wishlist_obj, created = Wishlist.objects.get_or_create(user=request.user)
    products = wishlist_obj.products.all().order_by('-id')

    context = {
        'wishlist': wishlist_obj,
        'products': products,
    }
    return render(request, 'store/wishlist.html', context)

@login_required
@require_POST
def add_to_wishlist(request, product_id):
    """Add a product to the user's wishlist."""
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)

    if product not in wishlist.products.all():
        wishlist.products.add(product)
        messages.success(request, f'{product.name} added to your wishlist.')

    return redirect('store:product_detail', product_slug=product.slug)

@login_required
@require_POST
def remove_from_wishlist(request, product_id):
    """Remove a product from the user's wishlist."""
    product = get_object_or_404(Product, id=product_id)
    wishlist = Wishlist.objects.filter(user=request.user).first()

    if wishlist and product in wishlist.products.all():
        wishlist.products.remove(product)
        messages.success(request, f'{product.name} removed from your wishlist.')

    next_url = request.POST.get('next', 'store:wishlist')
    return redirect(next_url)