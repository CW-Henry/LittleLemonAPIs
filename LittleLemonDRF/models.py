from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# class Book(models.Model):
#     title = models.CharField(max_length=255)
#     author = models.CharField(max_length=255)
#     price = models.DecimalField(max_digits=5, decimal_places=2)

#     class Meta:
#         indexes = [
#             models.Index(fields=['price']),
#         ]


class Category(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.title


# class Rating(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     menuitem_id = models.SmallIntegerField()
#     rating = models.SmallIntegerField()


class MenuItem(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.SmallIntegerField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=1)

    def __str__(self) -> str:
        return self.title


class Cart(models.Model):
    menuitem = models.ForeignKey(MenuItem,
                                 on_delete=models.PROTECT,
                                 null=False)
    user_id = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                null=False,
                                db_column="user_id")


class Orders(models.Model):
    orderitem = models.ForeignKey(MenuItem,
                                  on_delete=models.PROTECT,
                                  null=False,
                                  db_column="order_item_id")
    user_id = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                null=False,
                                db_column="user_id")
    delivery_status = models.SmallIntegerField(choices=[(0, 0), (1, 1)],
                                               null=True)
