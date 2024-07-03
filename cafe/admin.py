from django.contrib import admin
from cafe.models import (
    Cafe,
    Cuisine,
    EstablishmentType,
    CafeLunchMenu,
    LunchDish
)

models = [Cuisine, EstablishmentType, LunchDish]
for model in models:
    admin.site.register(model)


class LunchDishInline(admin.TabularInline):
    fk_name = 'menu'
    model = LunchDish
    extra = 5


@admin.register(CafeLunchMenu)
class ProductAdmin(admin.ModelAdmin):
    exclude = ["article"]
    inlines = [LunchDishInline]
    list_filter = ('cafe',)
    search_fields = ("cafe__name", "cafe__id")


class LunchMenuInline(admin.TabularInline):
    fk_name = 'cafe'
    model = CafeLunchMenu
    extra = 7


@admin.register(Cafe)
class ProductAdmin(admin.ModelAdmin):
    exclude = ["article"]
    inlines = [LunchMenuInline]
