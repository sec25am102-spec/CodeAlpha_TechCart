from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Product, Order, OrderItem


def home(request):
    products = Product.objects.all()

    search = request.GET.get('search')
    if search:
        products = products.filter(name__icontains=search)

    return render(request, 'home.html', {'products': products})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})


def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1

    request.session['cart'] = cart
    return redirect('cart')


def cart(request):
    cart = request.session.get('cart', {})
    products = []

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        total = product.price * quantity

        products.append({
            'product': product,
            'quantity': quantity,
            'total': total
        })

    grand_total = sum(item['total'] for item in products)

    return render(request, 'cart.html', {
        'products': products,
        'grand_total': grand_total
    })


def increase_quantity(request, product_id):
    cart = request.session.get('cart', {})
    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] += 1

    request.session['cart'] = cart
    return redirect('cart')


def decrease_quantity(request, product_id):
    cart = request.session.get('cart', {})
    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] -= 1

        if cart[product_id] <= 0:
            del cart[product_id]

    request.session['cart'] = cart
    return redirect('cart')


def checkout(request):
    cart = request.session.get('cart', {})
    products = []

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        total = product.price * quantity

        products.append({
            'product': product,
            'quantity': quantity,
            'total': total
        })

    grand_total = sum(item['total'] for item in products)

    return render(request, 'checkout.html', {
        'products': products,
        'grand_total': grand_total
    })


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        login(request, user)
        return redirect('home')

    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('home')

        messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


def place_order(request):
    if request.method != 'POST':
        return redirect('checkout')

    cart = request.session.get('cart', {})

    if not cart:
        return redirect('cart')

    customer_name = request.POST.get('customer_name')
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    address = request.POST.get('address')

    products = []
    grand_total = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)

        total = product.price * quantity
        grand_total += total

        products.append({
            'product': product,
            'quantity': quantity,
            'total': total
        })

    order = Order.objects.create(
        customer_name=customer_name,
        email=email,
        phone=phone,
        address=address,
        total_amount=grand_total
    )

    for item in products:
        OrderItem.objects.create(
            order=order,
            product=item['product'],
            quantity=item['quantity'],
            price=item['product'].price
        )

    request.session['cart'] = {}

    return render(request, 'order_success.html', {
        'order': order
    })