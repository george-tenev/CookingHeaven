from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from CookingHeaven.common.view_mixins import AdminRequiredMixin, PermissionRequiredHomeRedirectMixin
from CookingHeaven.main.forms import CategoryCreateForm
from CookingHeaven.main.models import Category


class CategoryCreateView(LoginRequiredMixin, AdminRequiredMixin, PermissionRequiredHomeRedirectMixin, CreateView):
    model = Category
    form_class = CategoryCreateForm
    template_name = 'admin/category_create.html'
    success_url = reverse_lazy('dashboard')
    permission_required = 'main.add_category'

class CategoryUpdateView(LoginRequiredMixin, AdminRequiredMixin, PermissionRequiredHomeRedirectMixin, UpdateView):
    model = Category
    form_class = CategoryCreateForm
    template_name = 'admin/category_update.html'
    success_url = reverse_lazy('dashboard')
    permission_required = 'main.change_category'


class CategoryDeleteView(LoginRequiredMixin, AdminRequiredMixin, PermissionRequiredHomeRedirectMixin, DeleteView):
    model = Category
    success_url = reverse_lazy('dashboard')
    permission_required = 'main.delete_category'


class CategoryListView(LoginRequiredMixin, PermissionRequiredHomeRedirectMixin, ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'admin/category_list.html'
    permission_required = 'main.view_category'
