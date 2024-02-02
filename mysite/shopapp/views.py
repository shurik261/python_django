"""
В этом модуле лежат различные наборы представлений.

Разные view для интернет-магазина: по товарам, заказам и т.д.
"""
import logging
from timeit import default_timer
from django.contrib.auth.models import Group
from django.http import HttpRequest, HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, \
    CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, \
    PermissionRequiredMixin, UserPassesTestMixin, \
    PermissionDenied
from drf_spectacular.utils import OpenApiResponse, extend_schema

from rest_framework.request import Request
from rest_framework.response import Response
from .common import save_csv_products
from .models import Product, Order, ProductImage
from .forms import GroupForm, ProductForm
from rest_framework.parsers import MultiPartParser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from csv import DictWriter
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet
from .serializers import ProductSerializer, OrderSerializer

log = logging.getLogger(__name__)


@extend_schema(description='Product views CRUDE')
class ProductViewSet(ModelViewSet):
    """
    Набор представлений для действий над Product.

    Полный CRUD для сущностей товара
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    search_fields = ['name', 'description', ]
    filterset_fields = [
        'name', 'price', 'description', 'discount', 'archived',
    ]
    ordering_fields = ['pk', 'name', 'price', 'discount', ]

    @extend_schema(
        summary='Get one product by ID',
        description='Retrieves **product**, return 404 if not found',
        responses={
            200: ProductSerializer,
            404: OpenApiResponse(description='Empty response, product by id not found')
        },

    )
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)

    @action(methods=['get'], detail=False)
    def download_csv(self, request: Request):
        response = HttpResponse(content_type='text/csv')
        filename = 'import-products.csv'
        response['Content-Desposition'] = f'Attachment; filename={filename}'
        queryset = self.filter_queryset(self.get_queryset())
        fields = [
            'name',
            'description',
            'price',
            'discount',
        ]
        queryset = queryset.only(*fields)
        writer = DictWriter(response, fieldnames=fields)
        writer.writeheader()

        for product in queryset:
            writer.writerow({
                field: getattr(product, field)
                for field in fields
            })
        return response

    @action(
        detail=False,
        methods=['post'],
        parser_classes=[MultiPartParser],
    )
    def upload_csv(self, request: Request):
        products = save_csv_products(
            request.FILES['files'].file,
            encoding=request.encoding
        )
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)


class OrderViewSet(ModelViewSet):
    """
    Вьюсет (ViewSet) для работы с заказами.

    Позволяет выполнять операции CRUD (Create, Retrieve, Update, Delete)
    над заказами.
    """

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    search_fields = ['user', 'products', 'delivery_address', 'promocode', ]
    filterset_fields = ['user', 'products', 'delivery_address', 'promocode', ]
    ordering_fields = ['pk', 'user', 'products', 'delivery_address', ]


class ShopIndexView(View):
    """
    Класс ShopIndexView является представлением на основе классов в Django.

    Он предназначен для обработки HTTP GET-запросов и
    отображения страницы магазина.
    """

    def get(self, request: HttpRequest):
        """
        Этот метод обрабатывает HTTP GET-запрос и возвращает HttpResponse.

        Он извлекает информацию о продуктах и автомобилях,
        подготавливает контекст и отображает HTML-шаблон
        'shopapp/shop-index.html' с предоставленным контекстом.
        """

        products = [
            ('Bmw', 15000),
            ('Toyota', 10000),
            ('Жигули', 2000),
        ]
        auto = [
            {'name': 'Bmw', 'price': 15000,
             'currency': '€', 'country': 'Германия'},
            {'name': 'Toyota', 'price': 10000, ''
                                               'currency': '$', 'country': 'Япония'},
            {'name': 'Жигули', 'price': 2000000,
             'currency': '₽', 'country': 'Россия'},
            {'name': 'Honda', 'price': 9000,
             'currency': '$', 'country': 'Япония'},
        ]
        context = {
            'time_running': default_timer,
            'products': products,
            'auto': auto
        }
        log.debug('Products for shop index. %s', products)
        log.info('Rendering shop index')
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
    # model = Product
    queryset = Product.objects.prefetch_related('images')
    template_name = 'shopapp/product-details.html'
    context_object_name = 'product'


class ProductListView(ListView):
    template_name = 'shopapp/products-list.html'
    # model = Product
    context_object_name = 'products'
    queryset = Product.objects.filter(archived=False)


class ProductCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'shopapp.add_product'

    model = Product
    fields = 'name', 'price', 'description', 'discount', 'preview'
    success_url = reverse_lazy('shopapp:products_list')


class ProductUpdateView(UserPassesTestMixin, UpdateView):
    def test_func(self):
        product = self.get_object()
        is_superuser = self.request.user.is_superuser
        has_permission = self.request.user.has_perm('shopapp.change_product')
        is_author = self.request.user == product.created_by
        if (is_superuser or (has_permission and is_author)):
            return True
        raise PermissionDenied(
            "You don't have permission to edit this product."
        )

    model = Product
    # fields = 'name', 'price', 'description', 'discount', 'preview'
    template_name_suffix = '_update_form'
    form_class = ProductForm

    def get_success_url(self):
        return reverse(
            'shopapp:products_details',
            kwargs={'pk': self.object.pk}
        )

    def form_valid(self, form):
        response = super().form_valid(form)
        for image in form.files.getlist('images'):
            ProductImage.objects.create(
                product=self.object,
                image=image
            )
        return response


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('shopapp:products_list')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class OrderListView(LoginRequiredMixin, ListView):
    queryset = (
        Order.objects.
            select_related('user').
            prefetch_related('products')
    )


class OrderDetailsView(PermissionRequiredMixin, DetailView):
    permission_required = 'shopapp.view_order'
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


class OrderExportView(View):

    def get(self, request: HttpRequest) -> JsonResponse:
        orders = Order.objects.order_by('pk').all()
        orders_data = [
            {
                'pk': order.pk,
                'delivery_address': order.delivery_address,
                'promocode': order.promocode,
                'user_id': order.user,
                'products_id': order.products,
            }
            for order in orders
        ]
        return JsonResponse({'orders': orders_data})
