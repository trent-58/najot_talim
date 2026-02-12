from django.db import models
from baseapp.models import BaseModel
from accounts.models import User

class Product(BaseModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return self.name

    def soft_delete_related(self, using=None):
        self.comments.update(is_deleted=True)
        self.cart_items.update(is_deleted=True)
        self.order_items.update(is_deleted=True)

    class Meta:
        ordering = ("-updated_at",)

class Comment(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()

    def __str__(self):
        return f"Comment #{self.pk} on {self.product}"

    class Meta:
        ordering = ("-updated_at",)
