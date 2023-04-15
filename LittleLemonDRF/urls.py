from django.urls import path
from . import views

urlpatterns = [
    # path('books', views.books),
    # path('books', views.BookView.as_view()),
    # path('books/<int:pk>', views.SingleBookView.as_view()),

    # path('category', views.CategoriesView.as_view()),
    # path('category/<int:pk>', views.SingleCategoryView.as_view()),
    # path('ratings', views.RatingsView.as_view()),
    path('menu-items', views.MenuItemsView.as_view()),
    path('menu-items/<int:pk>', views.SingleMenuItemView.as_view()),
    path('groups/<str:name>/users', views.UserGroupView.as_view()),
    path('groups/<str:name>/users/<int:pk>',
         views.SingleUserGroupView.as_view()),
    path(
        'cart/menu-items',
        views.CartViewSet.as_view({
            'get': 'list',
            'post': 'create',
            'delete': 'destroy'
        }))
    # path('groups/manager', views)
]
