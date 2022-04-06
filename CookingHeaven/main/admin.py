from django.contrib import admin

from CookingHeaven.accounts.models import Profile, CookingHeavenUser
from CookingHeaven.main.models import Category, Recipe, RecipeStep, Unit, Ingredient


class ProfileInlineAdmin(admin.StackedInline):
    model = Profile

@admin.register(CookingHeavenUser)
class AppUserAdmin(admin.ModelAdmin):

    inlines = (ProfileInlineAdmin,)



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    pass




@admin.register(RecipeStep)
class RecipeStepAdmin(admin.ModelAdmin):
    pass

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    pass

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    pass




