from django.db import models


class SoftDeleteQuerySet(models.QuerySet):
    def delete(self, *args, **kwargs):
        deleted = 0
        for obj in self:
            obj.delete()
            deleted += 1
        return deleted, {self.model._meta.label: deleted}

class BaseModel(models.Model):
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save(update_fields=["is_deleted"], using=using)
        self.soft_delete_related(using=using)

    def soft_delete_related(self, using=None):
        pass

    objects = SoftDeleteQuerySet.as_manager()

    class Meta:
        abstract = True
        ordering = ("-updated_at",)
