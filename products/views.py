from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from .models import Product, Like
from .forms import ProductForm, CommentForm, UserRegistrationForm
from django.http import JsonResponse


def home(request):
    new_products = Product.objects.all().order_by('-created_at')[:3]
    all_products = Product.objects.all().order_by('-created_at')
    
    context = {
        'new_products': new_products,
        'all_products': all_products,
    }
    return render(request, 'products/home.html', context)

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProductForm()
    
    return render(request, 'products/add_product.html', {'form': form})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    comment_form = CommentForm()
    user_liked = False
    if request.user.is_authenticated:
        user_liked = product.likes.filter(user=request.user).exists()
    
    context = {
        'product': product,
        'comment_form': comment_form,
        'user_liked': user_liked,
    }
    return render(request, 'products/product_detail.html', context)

@login_required

@login_required
def like_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # This is an AJAX request
        liked = False
        if product.likes.filter(user=request.user).exists():
            product.likes.filter(user=request.user).delete()
        else:
            Like.objects.create(user=request.user, product=product)
            liked = True
        
        return JsonResponse({
            'liked': liked,
            'like_count': product.likes.count()
        })
    else:
        # Fallback for non-JS browsers
        if product.likes.filter(user=request.user).exists():
            product.likes.filter(user=request.user).delete()
        else:
            Like.objects.create(user=request.user, product=product)
        return redirect('product_detail', pk=pk)

@login_required
def add_comment(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.product = product
            comment.save()
    return redirect('product_detail', pk=pk)

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'products/register.html', {'form': form})