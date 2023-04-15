from rest_framework import serializers
from .models import MenuItem, Category, Cart, Order
from rest_framework.validators import UniqueTogetherValidator
from django.contrib.auth.models import User, Group

# class BookSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Book
#         fields = ['id', 'title', 'author', 'price']


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'title']


class MenuItemSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(write_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = MenuItem
        fields = [
            'id', 'title', 'price', 'inventory', 'category', 'category_id'
        ]
        extra_kwargs = {
            'price': {
                'min_value': 2
            },
            'inventory': {
                'min_value': 0
            }
        }


# class RatingSerializer(serializers.ModelSerializer):
#     user = serializers.PrimaryKeyRelatedField(
#         queryset=User.objects.all(), default=serializers.CurrentUserDefault())

#     class Meta:
#         model = Rating
#         fields = ['user', 'menuitem_id', 'rating']

#     validators = [
#         UniqueTogetherValidator(queryset=Rating.objects.all(),
#                                 fields=['user', 'menuitem_id'])
#     ]

#     extra_kwargs = {
#         'rating': {
#             'min_value': 0,
#             'max_value': 5
#         },
#     }


class UserGroupSerializer(serializers.ModelSerializer):
    # group = Group

    class Meta:
        model = User
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    menuitem = MenuItemSerializer()

    # user = UserGroupSerializer(many=True)
    class Meta:
        model = Cart
        fields = ['menuitem', 'user_id']
        extra_kwargs = {'user_id': {'read_only': True}}


class OrdersManageSerializer(serializers.ModelSerializer):
    order_item = MenuItemSerializer()

    # user = UserGroupSerializer(many=True)
    class Meta:
        model = Order
        fields = '__all__'
        extra_kwargs = {'user_id': {'read_only': True}}
