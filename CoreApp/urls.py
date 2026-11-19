

from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_view, name='home'),
    path('books/', views.books_view, name='books'),
    path('used-books/', views.used_books_view, name='used_books'),
    path('used-books/edit/<int:book_id>/', views.edit_used_book, name='edit_used_book'),
    path('about/',views.about_view, name='about'),
    path('contact/',views.contact_view, name='contact'),
    path('book-detail/', views.book_detail_view, name='book_detail'),
    path('book/<int:book_id>/', views.book_detail_view, name='book_detail'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('account/', views.account_view, name='account'),
    path('add-to-cart/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/update/<int:item_id>/<str:action>/', views.update_quantity, name='update_quantity'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('used-books/add/', views.add_used_book, name='add_used_book'),
    path('used-books/rent/<int:book_id>/', views.rent_book, name='rent_book'),
    path(
    'used-books/rental/return/<int:rental_id>/',
        views.mark_as_returned,name='mark_as_returned'
    ),
    path('chat/<int:book_id>/',views.chat_view,name='chat'
    ),
    path(
    'wishlist/toggle/<int:book_id>/',
    views.toggle_wishlist,
    name='toggle_wishlist'
    ),
    path(
    'wishlist/',
    views.wishlist_view,
    name='wishlist'
    ),


    ]