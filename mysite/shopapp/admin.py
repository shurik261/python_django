from django.contrib import admin
from django.shortcuts import render, redirect

from .common import save_csv_products
from .models import Product, Order, ProductImage
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from .admin_mixins import ExportAsCSVMixin
from .forms import CSVImportForm
from django.urls import path


class OrderInLine(admin.TabularInline):
    model = Product.orders.through


class ProductInLine(admin.StackedInline):
    model = ProductImage


@admin.action(description='Archiv products')
def mark_archived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=True)


@admin.action(description='Unarchiv products')
def mark_unarchived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    queryset.update(archived=False)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    change_list_template = 'shopapp/products_changelist.html'
    actions = [
        mark_archived,
        mark_unarchived,
        'export_csv',
    ]
    inlines = [
        OrderInLine,
        ProductInLine,
    ]
    list_display = 'pk', 'name', 'description_short', 'price', 'discount', 'archived'
    list_display_links = 'pk', 'name'
    ordering = 'pk', 'name'
    search_fields = 'name', 'description'
    fieldsets = [
        (None, {
            'fields': ('name', 'description')
        }),
        ('Price options', {
            'fields': ('price', 'discount'),
            'classes': ('wide', 'collapse')
        }),
        ('Image', {
            'fields': ('preview',),

        }),
        ('Extra options', {
            'fields': ('archived',),
            'classes': ('collapse',),
            'description': 'Field "archived" is for soft delete'
        })
    ]

    # admin.site.register(Product, ProductAdmin)
    def description_short(self, obj: Product):
        if len(obj.description) < 48:
            return obj.description
        return obj.description[:48] + '...'

    def import_csv(self, request: HttpRequest) -> HttpResponse:
        if request.method == 'GET':
            form = CSVImportForm()
            context = {
                'form': form,
            }
            return render(request, 'admin/csv_form.html', context)
        form = CSVImportForm(request.POST, request.FILES)
        if not form.is_valid():
            form = CSVImportForm()
            context = {
                'form': form,
            }
            return render(request, 'admin/csv_form.html', context, status=400)
        save_csv_products(
            file=form.files['csv_file'].file,
            encoding=request.encoding
        )

        self.message_user(request, 'Data from CSV was imported')
        return redirect('..')
    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path(
                'import-products-csv/',
                self.import_csv,
                name='import_products_csv'
            )
        ]
        return new_urls + urls


class ProductInLine(admin.StackedInline):
    model = Order.products.through


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        ProductInLine,
    ]
    list_display = 'delivery_address', 'promocode', 'created_at', 'user_verbose'

    def get_queryset(self, request):
        return Order.objects.select_related('user').prefetch_related('products')

    def user_verbose(self, obj: Order) -> str:
        return obj.user.first_name or obj.user.username
