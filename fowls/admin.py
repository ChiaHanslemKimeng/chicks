from django.contrib import admin
from .models import Category, Breed, Product, ProductImage

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'slug')
    list_filter = ('category',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'breed', 'price', 'availability', 'created_at')
    list_filter = ('category', 'breed', 'availability', 'created_at')
    search_fields = ('name', 'description')
    inlines = [ProductImageInline]
