from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField()
    image = models.URLField()
    preview_link = models.URLField(blank=True)

    def __str__(self):
        return self.title


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=30, default='Placed')

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.book.title} - Order #{self.order.id}"


class UsedBook(models.Model):
    CONDITION_CHOICES = [
        ('Like New', 'Like New'),
        ('Very Good', 'Very Good'),
        ('Good', 'Good'),
        ('Fair', 'Fair'),
    ]

    LISTING_TYPE_CHOICES = [
        ('Sell', 'Sell'),
        ('Rent', 'Rent'),
    ]

    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    condition = models.CharField(
        max_length=20,
        choices=CONDITION_CHOICES
    )
    price = models.DecimalField(max_digits=8, decimal_places=2)
    listing_type = models.CharField(
        max_length=10,
        choices=LISTING_TYPE_CHOICES
    )
    description = models.TextField()
    image = models.ImageField(upload_to='used_books/')

    def __str__(self):
        return self.title


class Rental(models.Model):
    renter = models.ForeignKey(User, on_delete=models.CASCADE)
    used_book = models.ForeignKey(UsedBook, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    rental_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, default='Active')

    def __str__(self):
        return f"{self.used_book.title} - {self.renter.username}"

class Message(models.Model):
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )

    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_messages'
    )

    book = models.ForeignKey(
        UsedBook,
        on_delete=models.CASCADE
    )

    message = models.TextField()

    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} → {self.receiver.username}"

class Wishlist(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE
    )

    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"