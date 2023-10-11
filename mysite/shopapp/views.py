from timeit import default_timer

from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Product, Order
from .forms import GroupForm

class ShopIndexView(View):
    def get(self, request: HttpRequest):
        products = [
            ('Bmw', 15000),
            ('Toyota', 10000),
            ('Жигули', 2000),
        ]
        auto = [
            {'name': 'Bmw','price': 15000, 'currency': '€', 'country': 'Германия'},
            {'name': 'Toyota', 'price': 10000, 'currency': '$','country': 'Япония'},
            {'name': 'Жигули', 'price': 2000000, 'currency': '₽','country': 'Россия'},
            {'name': 'Honda', 'price': 9000, 'currency': '$', 'country': 'Япония'},
        ]
        context = {
            'time_running': default_timer,
            'products': products,
            'auto': auto
        }
        return render(request, 'shopapp/shop-index.html', context=context)

class GroupsListView(View):
    def get(self, request: HttpRequest):
        context = {
            'form': GroupForm(),
            'groups': Group.objects.prefetch_related('permissions').all(),
        }
        return render(request, 'shopapp/groups-list.html', context=context)
    def post(self, request: HttpRequest):
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(request.path)
class ProductDetailsView(DetailView):
    template_name = 'shopapp/product-details.html'
    model = Product
    context_object_name = 'product'

class ProductListView(ListView):
    template_name = 'shopapp/products-list.html'
    # model = Product
    context_object_name = 'products'
    queryset = Product.objects.filter(archived=False)

class ProductCreateView(CreateView):
    model = Product
    fields = 'name', 'price', 'description', 'discount',
    success_url = reverse_lazy('shopapp:products_list')

class ProductUpdateView(UpdateView):
    model = Product
    fields = 'name', 'price', 'description', 'discount',
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse(
            'shopapp:products_details',
            kwargs={'pk': self.object.pk}
        )

class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('shopapp:products_list')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)

class OrderListView(ListView):
    queryset = (
        Order.objects.
        select_related('user').
        prefetch_related('products')
    )

class OrderDetailsView(DetailView):
    queryset = (
        Order.objects.
        select_related('user').
        prefetch_related('products')
    )
class OrderCreateView(CreateView):
    model = Order
    fields = 'user', 'products', 'delivery_address', 'promocode'
    success_url = reverse_lazy('shopapp:orders_list')

class OrderUpdateView(UpdateView):
    model = Order
    fields = 'user', 'products', 'delivery_address', 'promocode'
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse(
            'shopapp:orders_details',
            kwargs={'pk': self.object.pk}
        )
class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy('shopapp:orders_list')