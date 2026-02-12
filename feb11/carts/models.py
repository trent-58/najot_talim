from django.db import models
from baseapp.models import BaseModel
from accounts.models import User
from products.models import Product


class Cart(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="carts")
    checked_out_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Cart #{self.pk} for {self.user}"

    def soft_delete_related(self, using=None):
        self.items.update(is_deleted=True)

    class Meta:
        ordering = ("-updated_at",)


class CartItem(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cart_items")
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product}"

    class Meta:
        ordering = ("-updated_at",)
