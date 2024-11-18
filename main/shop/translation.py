from .models import Product
from modeltranslation.translator import TranslationOptions,register

@register(Product)
class ProductTranslation(TranslationOptions):
    fields = ('product_name', 'description')