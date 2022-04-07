from django.urls import path, include

from CookingHeaven.accounts import admin
from CookingHeaven.main import views
from CookingHeaven.main.views import generic, category, admin_panel, unit, err
from CookingHeaven.main.views import recipe

urlpatterns = [
    path('', generic.IndexTemplateView.as_view(), name='home'),
    path('dashboard/', generic.DashboardView.as_view(), name='dashboard'),

    path('recipe/create/', recipe.RecipeCreateView.as_view(), name='recipe create'),
    path('recipe/update/<int:pk>/', recipe.RecipeUpdateView.as_view(), name='recipe update'),
    path('recipe/delete/<int:pk>/', recipe.RecipeDeleteView.as_view(), name='recipe delete'),
    path('recipe/details/<int:pk>/', recipe.RecipeDetailsView.as_view(), name='recipe details'),
    path('recipe/like/<int:pk>/', recipe.LikeButtonView.as_view(), name='recipe like'),

    path('category/create/', category.CategoryCreateView.as_view(), name='category create'),
    path('category/list/', category.CategoryListView.as_view(), name='category list'),
    path('category/update/<int:pk>', category.CategoryUpdateView.as_view(), name='category update'),
    path('category/delete/<int:pk>', category.CategoryDeleteView.as_view(), name='category delete'),

    path('unit/create/', unit.UnitCreateView.as_view(), name='unit create'),
    path('unit/list/', unit.UnitListView.as_view(), name='unit list'),
    path('unit/update/<int:pk>', unit.UnitUpdateView.as_view(), name='unit update'),
    path('unit/delete/<int:pk>', unit.UnitDeleteView.as_view(), name='unit delete'),

    path('400/', err.bad_request, name= '400'),
    path('500/', err.internal_error, name='500'),

    path('admin-panel/', admin_panel.AdminPanelView.as_view(), name='admin panel')

]