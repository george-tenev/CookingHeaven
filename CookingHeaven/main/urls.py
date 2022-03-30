from django.urls import path, include

from CookingHeaven.accounts import admin
from CookingHeaven.main import views
from CookingHeaven.main.views import generic, food_type, admin_panel, ingredient
from CookingHeaven.main.views import recipe

urlpatterns = [
    path('', generic.IndexTemplateView.as_view(), name='home'),
    path('dashboard/', generic.DashboardView.as_view(), name='dashboard'),

    path('recipe/create/', recipe.RecipeCreateView.as_view(), name='recipe create'),
    path('recipe/update/<int:pk>/', recipe.RecipeUpdateView.as_view(), name='recipe update'),
    path('recipe/delete/<int:pk>/', recipe.RecipeDeleteView.as_view(), name='recipe delete'),
    path('recipe/details/<int:pk>/', recipe.RecipeDetailsView.as_view(), name='recipe details'),
    path('recipe/like/<int:pk>/', recipe.like_button, name='recipe like'),

    path('food_type/create/', food_type.FoodtypeCreateView.as_view(), name='food type create'),

    path('htmx/ingredient-create-form/', ingredient.IngredientCreateView.as_view(), name='ingredient create form'),

    path('admin-panel/', admin_panel.AdminPanelView.as_view(), name='admin panel')

]