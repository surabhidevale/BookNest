from django.contrib import admin
from .models import Book, CartItem,Order,OrderItem,UsedBook,Rental,Message,Wishlist

admin.site.register(Book)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(UsedBook)
admin.site.register(OrderItem)
admin.site.register(Rental)
admin.site.register(Message)
admin.site.register(Wishlist)