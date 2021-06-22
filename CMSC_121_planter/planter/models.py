from django.db import models

class Item(models.Model):
    item_name = models.CharField(max_length=100)
    price = models.FloatField()
    image = models.ImageField(upload_to = '', default= 'products/default.jpeg')
    discount_price = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY, max_length=2)
    label = models.CharField(choices=LABEL, max_length=2)
    group = models.CharField(choices=GROUP, max_length=2, default="")
    description = models.TextField()
    
    def __str__(self):
        return self.item_name

    def get_absolute_url(self):
        return reverse("product", kwargs={
            "pk" : self.pk
        
        })

    def get_add_to_cart_url(self):
        return reverse("add-to-cart", kwargs={
            "pk" : self.pk
        })

    def get_remove_from_cart_url(self):
        return reverse("remove-from-cart", kwargs={
            "pk" : self.pk
        })
  

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.item_name}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_discount_item_price()
        return self.get_total_item_price()

    #def get_delivery_fee(self):
    #    return self.item.delivery_fee

    #def get_price_with_delivery(self):
    #    return self.get_delivery_fee()
    

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    checkout_address = models.ForeignKey(
        'CheckoutAddress', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey(
        'Payment', on_delete=models.SET_NULL, blank=True, null=True)
    payment_checkout = models.ForeignKey(
        'PaymentCheckout', on_delete=models.SET_NULL, blank=True, null=True)
    delivery_fee = models.FloatField(default=0)

    def __str__(self):
        return self.user.username
    
    def get_total_price(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total

    def get_delivery_fee(self):
       return self.delivery_fee

    def get_price_with_delivery(self):
        total = self.get_total_price() + self.get_delivery_fee()
        return total


class CheckoutAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    shipping_street_address = models.CharField(max_length=100, default='DEFAULT VALUE')
    shipping_apartment_address = models.CharField(max_length=100, default='DEFAULT VALUE')
    billing_street_address = models.CharField(max_length=100, default='DEFAULT VALUE')
    billing_apartment_address = models.CharField(max_length=100, default='DEFAULT VALUE')
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=100)
    customer_name = models.CharField(max_length=100, default='DEFAULT VALUE')
    contact_number = models.CharField(max_length=100, default='DEFAULT VALUE')
    shipping_option = models.CharField(max_length=100, default='DEFAULT VALUE')
    payment_option = models.CharField(max_length=100, default='DEFAULT VALUE')

    def __str__(self):
        return self.user.username
    
class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class PaymentCheckout(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    account_name = models.CharField(max_length=100, default='DEFAULT VALUE')
    account_number = models.CharField(max_length=11, default='DEFAULT VALUE')

    def __str__(self):
        return self.user.username