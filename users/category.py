from django.db import models


class Category(models.Model):
    name = models.CharField(
        max_length=24, null=False, unique=True, verbose_name="Category"
    )
    user = models.CharField(max_length=24, null=False)
    # plural eg. band for musician
    users = models.CharField(max_length=24, null=True)
    # use for subcategories eg. painting as a subcategory of art
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="subcategoryId",
    )

    def __str__(self):
        return self.name
