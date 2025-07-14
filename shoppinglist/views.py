from django.views import View
from django.views.generic import TemplateView, ListView, DeleteView
from django.views.generic.edit import FormView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils import timezone
from collections import defaultdict
from .models import ShoppingItem, Category
from django.urls import reverse_lazy

class ShoppingListView(LoginRequiredMixin, View):
    template_name = 'shopping_list.html'

    def get(self, request, selected_category=None):
        categories = Category.objects.all()

        # Jeśli wybrano kategorię, filtrujemy produkty
        if selected_category:
            items = ShoppingItem.objects.filter(
                user=request.user, bought=False, category_id=selected_category
            ).select_related('category')
        else:
            items = ShoppingItem.objects.filter(
                user=request.user, bought=False
            ).select_related('category')

        categorized_items = defaultdict(list)
        for item in items:
            category_name = item.category.name if item.category else 'Inne'
            categorized_items[category_name].append(item)

        return render(request, self.template_name, {
            'items': items,
            'categories': categories,
            'categorized_items': dict(categorized_items),
            'selected_category': int(selected_category) if selected_category else None,
        })

    def post(self, request):
        name = request.POST.get('name')
        quantity = request.POST.get('quantity') or 1
        unit = request.POST.get('unit') or 'szt'
        category_id = request.POST.get('category')

        category = Category.objects.filter(id=category_id).first() if category_id else None

        if name:
            ShoppingItem.objects.create(
                name=name,
                quantity=quantity,
                unit=unit,
                category=category,
                user=request.user
            )

        # Po dodaniu renderujemy stronę GET z wybraną kategorią, by zapamiętać wybór
        return self.get(request, selected_category=category_id)


class MarkAsBoughtView(LoginRequiredMixin, View):
    def post(self, request, item_id):
        item = get_object_or_404(ShoppingItem, id=item_id, user=request.user)
        item.bought = True
        item.bought_at = timezone.now()
        item.save()
        return redirect('shopping_list')


class ToggleInCartView(LoginRequiredMixin, View):
    def post(self, request, item_id):
        item = get_object_or_404(ShoppingItem, id=item_id, user=request.user)
        item.in_cart = not item.in_cart
        item.save()
        return redirect('shopping_list')

class ShoppingHistoryView(LoginRequiredMixin, ListView):
    model = ShoppingItem
    template_name = 'shopping_history.html'
    context_object_name = 'bought_items'
    ordering = ['-bought_at']

    def get_queryset(self):
        return ShoppingItem.objects.filter(
            user=self.request.user,
            bought=True
        ).order_by('-bought_at')

class ShoppingItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ShoppingItem
    template_name = 'shoppingitem_confirm_delete.html'  # możesz stworzyć prosty szablon potwierdzenia lub pominąć
    success_url = reverse_lazy('shopping_history')

    def test_func(self):
        item = self.get_object()
        return item.user == self.request.user