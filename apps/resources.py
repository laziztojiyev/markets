from import_export.resources import ModelResource

from apps.models import Product


class ProductModelResource(ModelResource):
    class Meta:
        model = Product
