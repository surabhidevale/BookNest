
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Q
from datetime import timedelta
from django.utils import timezone
from .models import Book,CartItem,Order,OrderItem,UsedBook,Rental,Message,Wishlist
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def base_view (request):
    template_name ='CoreApp/base.html'
    context ={}
    return render(request,template_name,context)
def home_view(request):
    featured_books = Book.objects.all()[:4]

    return render(request, 'CoreApp/home.html', {
        'featured_books': featured_books
    })
def books_view(request):
    search = request.GET.get('search', '')
    category = request.GET.get('category', '')

    books = Book.objects.all()

    if search:
        books = books.filter(
            Q(title__icontains=search) |
            Q(author__icontains=search)
        )

    if category:
        books = books.filter(category=category)

    return render(request, 'CoreApp/books.html', {
        'books': books
    })
def about_view(request):
    template_name ='CoreApp/about.html'
    context ={}
    return render(request,template_name,context)

def contact_view(request):
    template_name ='CoreApp/contact.html'
    context ={}
    return render(request,template_name,context)
def book_detail_view(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    is_wishlisted = False

    if request.user.is_authenticated:
        is_wishlisted = Wishlist.objects.filter(
            user=request.user,
            book=book
        ).exists()

    # Recommended books from the same category
    recommended_books = Book.objects.filter(
        category=book.category
    ).exclude(
        id=book.id
    )[:4]

    return render(request, 'CoreApp/book_detail.html', {
        'book': book,
        'is_wishlisted': is_wishlisted,
        'recommended_books': recommended_books
    })
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return render(request, 'CoreApp/register.html', {
                'error': 'Username already exists. Please choose another username.'
            })

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect('login')

    return render(request, 'CoreApp/register.html')

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

        return render(request, 'CoreApp/login.html', {
            'error': 'Invalid username or password.'
        })

    return render(request, 'CoreApp/login.html')
def logout_view(request):
    logout(request)
    return redirect('home')
def account_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    my_listings = UsedBook.objects.filter(seller=request.user)

    orders = Order.objects.filter(
        user=request.user
    ).prefetch_related('orderitem_set')

    rentals = Rental.objects.filter(
        renter=request.user
    ).select_related('used_book')

    my_listing_rentals = Rental.objects.filter(
        used_book__seller=request.user
    ).select_related('used_book', 'renter')

    messages = Message.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).select_related(
        'sender',
        'receiver',
        'book'
    ).order_by('-sent_at')

    conversations = {}

    for message in messages:
        book_id = message.book.id

        if book_id not in conversations:
            conversations[book_id] = message

    conversations = list(conversations.values())

    return render(request, 'CoreApp/account.html', {
        'my_listings': my_listings,
        'orders': orders,
        'rentals': rentals,
        'my_listing_rentals': my_listing_rentals,
        'conversations': conversations
    })
def add_to_cart(request, book_id):
    if not request.user.is_authenticated:
        return redirect('login')

    book = get_object_or_404(Book, id=book_id)

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        book=book
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')

def cart_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    cart_items = CartItem.objects.filter(user=request.user)

    total = sum(
        item.book.price * item.quantity
        for item in cart_items
    )

    return render(request, 'CoreApp/cart.html', {
        'cart_items': cart_items,
        'total': total
    })
def update_quantity(request, item_id, action):
    if not request.user.is_authenticated:
        return redirect('login')

    cart_item = CartItem.objects.get(
        id=item_id,
        user=request.user
    )

    if action == 'increase':
        cart_item.quantity += 1
        cart_item.save()

    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

    return redirect('cart')


def remove_from_cart(request, item_id):
    if not request.user.is_authenticated:
        return redirect('login')

    cart_item = CartItem.objects.get(
        id=item_id,
        user=request.user
    )

    cart_item.delete()

    return redirect('cart')
def checkout(request):
    if not request.user.is_authenticated:
        return redirect('login')

    cart_items = CartItem.objects.filter(user=request.user)

    if not cart_items.exists():
        return redirect('cart')

    total = sum(
        item.book.price * item.quantity
        for item in cart_items
    )

    order = Order.objects.create(
        user=request.user,
        total_amount=total
    )

    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            book=item.book,
            quantity=item.quantity,
            price=item.book.price
        )

    cart_items.delete()

    return render(request, 'CoreApp/order_success.html', {
        'order': order
    })
def used_books_view(request):
    used_books = UsedBook.objects.all()

    return render(request, 'CoreApp/used_books.html', {
        'used_books': used_books
    })

def add_used_book(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        UsedBook.objects.create(
            seller=request.user,
            title=request.POST.get('title'),
            author=request.POST.get('author'),
            category=request.POST.get('category'),
            condition=request.POST.get('condition'),
            price=request.POST.get('price'),
            listing_type=request.POST.get('listing_type'),
            description=request.POST.get('description'),
            image=request.FILES.get('image')
        )

        return redirect('used_books')

    return render(request, 'CoreApp/add_used_book.html')
def edit_used_book(request, book_id):
    if not request.user.is_authenticated:
        return redirect('login')

    book = get_object_or_404(UsedBook, id=book_id)

    # Only the seller who created the listing can edit it
    if book.seller != request.user:
        return redirect('used_books')

    if request.method == 'POST':
        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.category = request.POST.get('category')
        book.condition = request.POST.get('condition')
        book.price = request.POST.get('price')
        book.listing_type = request.POST.get('listing_type')
        book.description = request.POST.get('description')

        if request.FILES.get('image'):
            book.image = request.FILES.get('image')

        book.save()

        return redirect('used_books')

    return render(request, 'CoreApp/edit_used_book.html', {
        'book': book
    })
def rent_book(request, book_id):
    if not request.user.is_authenticated:
        return redirect('login')

    book = get_object_or_404(UsedBook, id=book_id)

    # Only rental listings can be rented
    if book.listing_type != 'Rent':
        return redirect('used_books')

    # Seller cannot rent their own book
    if book.seller == request.user:
        return redirect('used_books')

    # Don't allow another active rental
    active_rental = Rental.objects.filter(
        used_book=book,
        status='Active'
    ).exists()

    if active_rental:
        return redirect('used_books')

    # Rental period = 7 days
    return_date = timezone.now().date() + timedelta(days=7)

    Rental.objects.create(
        renter=request.user,
        used_book=book,
        price=book.price,
        return_date=return_date
    )

    return redirect('account')

def mark_as_returned(request, rental_id):
    if not request.user.is_authenticated:
        return redirect('login')

    rental = get_object_or_404(Rental, id=rental_id)

    # Only the seller of the book can mark it as returned
    if rental.used_book.seller != request.user:
        return redirect('account')

    rental.status = 'Returned'
    rental.save()

    return redirect('account')
def chat_view(request, book_id):
    if not request.user.is_authenticated:
        return redirect('login')

    book = get_object_or_404(UsedBook, id=book_id)
    seller = book.seller

    if request.user == seller:
        other_user = None
    else:
        other_user = seller

    # Get messages for this specific book and current user
    messages = Message.objects.filter(
        book=book
    ).filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).select_related(
        'sender',
        'receiver',
        'book'
    ).order_by('sent_at')

    if request.method == 'POST':

        message_text = request.POST.get('message')

        if message_text:

            if request.user == seller:

                # Seller replies to the person who sent the latest message
                last_message = messages.last()

                if last_message:
                    receiver = last_message.sender
                else:
                    receiver = None

            else:
                receiver = seller

            if receiver and receiver != request.user:

                Message.objects.create(
                    sender=request.user,
                    receiver=receiver,
                    book=book,
                    message=message_text
                )

        return redirect('chat', book_id=book.id)

    return render(request, 'CoreApp/chat.html', {
        'book': book,
        'seller': seller,
        'other_user': other_user,
        'messages': messages
    })
def toggle_wishlist(request, book_id):
    if not request.user.is_authenticated:
        return redirect('login')

    book = get_object_or_404(Book, id=book_id)
    wishlist_item = Wishlist.objects.filter(
        user=request.user,
        book=book
    ).first()

    if wishlist_item:
        wishlist_item.delete()
    else:
        Wishlist.objects.create(
            user=request.user,
            book=book
        )

    if request.GET.get('next') == 'wishlist':
        return redirect('wishlist')

    return redirect('book_detail', book_id=book.id)
def wishlist_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    wishlist_items = Wishlist.objects.filter(
        user=request.user
    ).select_related('book')

    return render(request, 'CoreApp/wishlist.html', {
        'wishlist_items': wishlist_items
    })