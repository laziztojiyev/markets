from django import forms
from django.contrib import admin
from django.contrib.admin import StackedInline
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.urls import reverse
from django.utils.safestring import mark_safe
from import_export.admin import ImportExportModelAdmin
from mptt.admin import DraggableMPTTAdmin

from apps.models import Product, Category, ProductImage, User
from apps.resources import ProductModelResource


# from apps.tasks import send_new_product_notification


class CategoryModelForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ()


@admin.register(Category)
class CategoryMPTTModelAdmin(DraggableMPTTAdmin):
    mptt_level_indent = 20
    form = CategoryModelForm


# class ProductModelForm(forms.ModelForm):
#     specifications = HStoreFormField()
#
#     def clean(self):
#         return super().clean()
#
#     class Meta:
#         model = Product
#         exclude = ()


class ProductImageStackedInline(StackedInline):
    model = ProductImage
    min_num = 1
    extra = 0
    fields = ['image']


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    def form_description(self, obj):
        return mark_safe(obj.description)

    inlines = (ProductImageStackedInline,)
    list_display = ['id', 'name', 'form_description', 'price', 'quantity', 'category', 'image_show',
                    'created_at_product']
    search_fields = ['id', 'name']
    list_per_page = 10
    list_max_show_all = 20
    resource_class = ProductModelResource

    def response_post_save_add(self, request, obj):
        result = super().response_post_save_add(request, obj)
        url = request.build_absolute_uri(reverse('product_detail', kwargs={'pk': obj.pk}))
        # send_new_product_notification.delay(product_name=obj.name, url=url)
        return result

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super(ProductAdmin, self).get_queryset(request)

        #     return super(ProductAdmin, self).get_queryset(request)
        else:
            qs = super(ProductAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)

    def image_show(self, obj: Product):
        if obj.images.first():
            return mark_safe("<img src='{}' width='200' />".format(obj.images.first().image.url))

        return ''

    image_show.description = 'images'


@admin.register(User)
class BaseUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Personal info'),
         {'fields': ('first_name', 'last_name', 'email', 'avatar', 'workout', 'country', 'verified', 'banner')}),
        (('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'avatar'),
        }),
    )
    # inlines = (UserImageStackedInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)


admin.site.unregister(Group)
