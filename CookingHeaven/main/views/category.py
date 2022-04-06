from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from CookingHeaven.common.view_mixins import AdminPermissionsRequiredMixin
from CookingHeaven.main.forms import CategoryCreateForm
from CookingHeaven.main.models import Category


class CategoryCreateView(LoginRequiredMixin, AdminPermissionsRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Category
    form_class = CategoryCreateForm
    template_name = 'admin/category_create.html'
    success_url = reverse_lazy('dashboard')
    permission_required = 'main.add_category'