from django.contrib import admin
from .models import Breed, Fowl, FowlImage

class FowlImageInline(admin.TabularInline):
    model = FowlImage
    extra = 3

@admin.register(Breed)
class BreedAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Fowl)
class FowlAdmin(admin.ModelAdmin):
    list_display = ('name', 'breed', 'price', 'age', 'availability', 'created_at')
    list_filter = ('breed', 'availability', 'created_at')
    search_fields = ('name', 'description')
    inlines = [FowlImageInline]
