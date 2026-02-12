from django.db import models
from baseapp.models import BaseModel
from accounts.models import User
from products.models import Product


class Order(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    delivered_at = models.DateTimeField(null=True, blank=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.pk} for {self.user}"

    def soft_delete_related(self, using=None):
        self.items.update(is_deleted=True)

    class Meta:
        ordering = ("-updated_at",)


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="order_items")
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product}"

    class Meta:
        ordering = ("-updated_at",)
