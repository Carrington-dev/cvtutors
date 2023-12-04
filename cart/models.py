from django.db import models
from panel.models import Course, Product

# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now=True)
    

    def __str__(self):
        return self.cart_id
    
    @property
    def item_count(self):
        return self.cart_items.count()

    class Meta:
       
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'


class CartItem(models.Model):
    """Model definition for Cart Item."""

    course = models.ForeignKey(Course, related_name='cart_item',blank=True, null=True,   on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='product_items', blank=True, null=True,  on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, related_name="cart_items", on_delete=models.CASCADE)
    # variations = models.ManyToManyField(Variations, blank=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    # TODO: Define fields here

    class Meta:
        """Meta definition for Cart Item."""
        

        verbose_name = 'Item'
        verbose_name_plural = 'Items'

    def __str__(self):
        """Unicode representation of Cart Item."""
        return str(self.product)
    
    def sub_total(self):
        return self.quantity * self.product.price
    
    def sub_total_vat(self):
        return self.quantity * self.product.price * 1.15
