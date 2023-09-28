from django.db import models


# Create your models here.
# Categories Table
class Category(models.Model):
    category_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.category_name


# Products Table
class Product(models.Model):
    product_name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    stock_quantity = models.PositiveIntegerField()
    image_url = models.URLField()
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name


# TODO("Make customer The auth model")
class Customer(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)


# Orders Table
class Order(models.Model):
    user_id = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_choices=(
        ('pending', 'Pending'), ('processing', 'Processing'), ('shipped', 'Shipped'), ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled')), default='pending', max_length=255)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)


# OrderItems Table
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    item_price = models.DecimalField(max_digits=10, decimal_places=2)


# Reviews/Ratings Table
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    review_text = models.TextField()
    review_date = models.DateTimeField(auto_now_add=True)


# Addresses Table
class Address(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=255)


# Payment Methods Table
class PaymentMethod(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    cardholder_name = models.CharField(max_length=255)
    card_number = models.CharField(max_length=16)
    expiration_date = models.DateField()
    cvv = models.CharField(max_length=4)


# Cart Table
class Cart(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()


# Wishlist Table
class Wishlist(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


# Coupons/Discounts Table
class Coupon(models.Model):
    coupon_code = models.CharField(max_length=255)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    expiration_date = models.DateField()


# Shipping Information Table
class ShippingInformation(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    shipping_date = models.DateTimeField()
    tracking_number = models.CharField(max_length=255)
    delivery_status = models.CharField(max_length=255)


# Returns/Refunds Table
class Return(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    return_reason = models.TextField()
    return_date = models.DateTimeField(auto_now_add=True)
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2)


# Messages/Notifications Table
class Message(models.Model):
    sender = models.ForeignKey('auth.User', related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey('auth.User', related_name='received_messages', on_delete=models.CASCADE)
    message_text = models.TextField()
    message_date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)


class Payment(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class MpesaPayment(Payment):
    mpesa_payment_id = models.AutoField(primary_key=True)
    phone_number = models.CharField(max_length=20)
    transaction_id = models.CharField(max_length=255)


class PayPalPayment(Payment):
    paypal_payment_id = models.AutoField(primary_key=True)
    transaction_id = models.CharField(max_length=255)
    paypal_email = models.EmailField()


class VisaPayment(Payment):
    visa_payment_id = models.AutoField(primary_key=True)
    cardholder_name = models.CharField(max_length=255)
    card_number = models.CharField(max_length=16)
    expiration_date = models.DateField()
    cvv = models.CharField(max_length=4)
