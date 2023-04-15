from django.shortcuts import render, get_object_or_404
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from .models import MenuItem, Cart, Orders
from django.contrib.auth.models import User, Group
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from .serializers import MenuItemSerializer, CategorySerializer, UserGroupSerializer, CartSerializer, OrdersManageSerializer
from rest_framework import generics, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.http import Http404
# Create your views here.
# @csrf_exempt
# def books(request):
#     if request.method == 'GET':
#         books = Book.objects.all().values()
#         return JsonResponse({"books": list(books)})
#     elif request.method == 'POST':
#         title = request.POST.get('title')
#         author = request.POST.get('author')
#         price = request.POST.get('price')
#         book = Book(title=title, author=author, price=price)
#         try:
#             book.save()
#         except IntegrityError:
#             return JsonResponse(
#                 {
#                     'error': 'true',
#                     'message': 'required field missing'
#                 },
#                 status=400)

#         return JsonResponse(model_to_dict(book), status=201)

###
# class BookView(generics.ListCreateAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer

# class SingleBookView(generics.RetrieveUpdateAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer

# class CategoriesView(generics.ListCreateAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer

# class SingleCategoryView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer

# class RatingsView(generics.ListCreateAPIView):
#     queryset = Rating.objects.all()
#     serializer_class = RatingSerializer

#     def get_permissions(self):
#         if (self.request.method == 'GET'):
#             return []

#         return [IsAuthenticated()]


class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields = ['price', 'inventory']
    filterset_fields = ['price', 'inventory']
    search_fields = ['title']


class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


class UserGroupView(generics.ListCreateAPIView):
    # queryset = User.objects.all()
    serializer_class = UserGroupSerializer

    # lookup_url_kwarg = "name"
    def get_queryset(self):
        # user = User.objects.all()
        # name = Group.objects.get(pk=user.groups[0]).name
        # print(self.kwargs['name'].replace('-', ' ').capitalize())
        cleaned_kwarg = self.kwargs['name'].replace('-', ' ').capitalize()
        group_id = Group.objects.filter(name=cleaned_kwarg).values_list(
            'id', flat=True)[0]
        queryset = User.objects.filter(groups=group_id)
        return queryset


class SingleUserGroupView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserGroupSerializer

    def get_queryset(self):
        cleaned_kwarg = self.kwargs['name'].replace('-', ' ').capitalize()
        group_id = Group.objects.filter(name=cleaned_kwarg).values_list(
            'id', flat=True)[0]
        queryset = User.objects.filter(groups=group_id)
        return queryset


# class CartView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Cart.objects.all()
#     serializer_class = CartSerializer

#     def get_object(self):
#         queryset = self.get_queryset()
#         # obj = get_object_or_404(queryset, pk=1)
#         obj = Cart.objects.filter(pk=0)
#         return queryset

# class CartView(APIView):
#     authentication_classes = [authentication.TokenAuthentication]

#     permission_classes = [permissions.AllowAny]

#     def get(self, request):

#         cart_items = Cart.objects.all()
#         serialized_data = CartSerializer(cart_items).data
#         serialized_data['user_token'] = str(request.auth)
#         serialized_data['user'] = str(request.user)
#         # print(request.user)
#         # print(serialized_data['user_token'])
#         return Response({"cart": serialized_data})


# def post(self, request):
class CartViewSet(viewsets.ViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.AllowAny]
    serializer_class = CartSerializer

    def list(self, request):
        print(request.user)
        print(request.user.id)
        print(Cart.objects.filter(user_id=request.user.id))
        if request.auth == None:
            return Response({"Cart": "User Token Not Found"},
                            status=status.HTTP_403_FORBIDDEN)
        queryset = Cart.objects.filter(user_id=request.user.id)
        serializer = CartSerializer(queryset, many=True)
        try:
            first_data = serializer.data[0]
        except IndexError:
            return Response({"Status": "No Content"},
                            status=status.HTTP_404_NOT_FOUND)
        return Response({
            "user_id": first_data['user_id'],
            "user_token": str(request.auth),
            "Cart": [data['menuitem'] for data in serializer.data]
        })

    def create(self, request):
        if request.auth == None:
            return Response({"Cart": "User Token Not Found"},
                            status=status.HTTP_403_FORBIDDEN)
        data = request.data.copy()
        data['user_id'] = str(request.user.id)
        data['user_token'] = str(request.auth)
        serializer = CartSerializer(data=data)
        # serializer.is_valid()
        # print(serializer.errors)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"Cart": serializer.data},
                            status=status.HTTP_201_CREATED)
        return Response({"Status": "Creation Failed"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request):
        if request.auth == None:
            return Response({"Cart": "User Token Not Found"},
                            status=status.HTTP_403_FORBIDDEN)
        Cart.objects.filter(user_id=request.user.id).delete()
        return Response({"Status": "Flushed Cart"},
                        status=status.HTTP_204_NO_CONTENT)


class OrdersManageView(generics.ListCreateAPIView):
    serializer_class = OrdersManageSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.AllowAny]

    def list(self, request):
        if request.auth == None:
            return Response({"Cart": "User Token Not Found"},
                            status=status.HTTP_403_FORBIDDEN)
        else:
            return super().list(request)

    def get_queryset(self):
        # print(Orders.objects.all())
        return Orders.objects.filter(user_id=self.request.user.id)

    def perform_create(self, serializer):
        cart_queryset = Cart.objects.filter(user_id=self.request.user.id)
        for item in cart_queryset:
            item['user_id'] = self.request.user.id
            item['delivery_status'] = 0
            s = OrdersManageSerializer(data=item)
            if s.is_valid():
                s.save()


class SingleOrderManageView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrdersManageSerializer
    queryset = Orders.objects.all()
    lookup_url_kwarg = "order_id"

    def get_queryset(self):
        # print(Orders.objects.all())
        return Orders.objects.filter(user_id=self.request.user.id)

    def perform_update(self, serializer):
        if self.request.user.groups.values_list('name',
                                                flat=True) == 'Delivery crew':
            data = self.request.data.copy()
            for index, item in enumerate(data):
                if index != 'delivery_status':
                    del data[index]
            s = OrdersManageSerializer(data=data)
            if s.is_valid(raise_exception=True):
                s.save()
                return Response({"Order": serializer.data},
                                status=status.HTTP_204_NO_CONTENT)
        else:
            return super().perform_update()
