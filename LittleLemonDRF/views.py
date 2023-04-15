from django.shortcuts import render, get_object_or_404
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from .models import MenuItem, Cart
from django.contrib.auth.models import User, Group
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from .serializers import MenuItemSerializer, CategorySerializer, UserGroupSerializer, CartSerializer
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
        if request.auth == None:
            return Response({"Cart": "User Token Not Found"},
                            status=status.HTTP_404_NOT_FOUND)
        queryset = Cart.objects.filter(user_token=request.auth)
        serializer = CartSerializer(queryset, many=True)
        return Response({"Cart": serializer.data})

    def create(self, request):
        if request.auth == None:
            return Response({"Cart": "User Token Not Found"},
                            status=status.HTTP_404_NOT_FOUND)
        CartSerializer(data=request.data).save()
        return Response({"Cart": "Created"}, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        if request.auth == None:
            return Response({"Cart": "User Token Not Found"},
                            status=status.HTTP_404_NOT_FOUND)