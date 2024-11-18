from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from .models import *

admin.site.register(Profile)
admin.site.register(Categories)


class PhotosInline(admin.TabularInline):
    model = ProductPhotos
    extra = 1
@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    group_fieldsets = True
    inlines = [PhotosInline]

    list_display = ("product_name", "description")

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }
admin.site.register(Rating)
admin.site.register(Review)
admin.site.register(CartItem)
admin.site.register(Cart)
