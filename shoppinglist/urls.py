from django.contrib import admin
from django.urls import path
from .views import ShoppingListView, MarkAsBoughtView, ToggleInCartView, ShoppingHistoryView, ShoppingItemDeleteView
from django.contrib.auth.views import LogoutView, LoginView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ShoppingListView.as_view(), name='shopping_list'),
    path('mark-bought/<int:item_id>/', MarkAsBoughtView.as_view(), name='mark_bought'),
    path('toggle-in-cart/<int:item_id>/', ToggleInCartView.as_view(), name='toggle_in_cart'),
    path('history/', ShoppingHistoryView.as_view(), name='shopping_history'),
    path('history/delete/<int:pk>/', ShoppingItemDeleteView.as_view(), name='delete_item'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]