from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Permission
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from CookingHeaven.common.view_mixins import AdminRequiredMixin, PermissionRequiredHomeRedirectMixin
from CookingHeaven.main.forms import UnitCreateForm
from CookingHeaven.main.models import Unit


class UnitCreateView(LoginRequiredMixin, AdminRequiredMixin, PermissionRequiredHomeRedirectMixin, CreateView):
    model = Unit
    form_class = UnitCreateForm
    template_name = 'admin/unit_create.html'
    success_url = reverse_lazy('dashboard')
    permission_required = 'main.add_unit'

class UnitUpdateView(LoginRequiredMixin, AdminRequiredMixin, PermissionRequiredHomeRedirectMixin, UpdateView):
    model = Unit
    form_class = UnitCreateForm
    template_name = 'admin/unit_update.html'
    success_url = reverse_lazy('dashboard')
    permission_required = 'main.change_unit'

class UnitDeleteView(LoginRequiredMixin, AdminRequiredMixin, PermissionRequiredHomeRedirectMixin, DeleteView):
    model = Unit
    success_url = reverse_lazy('dashboard')
    permission_required = 'main.delete_unit'


class UnitListView(LoginRequiredMixin, PermissionRequiredHomeRedirectMixin, ListView):
    model = Unit
    context_object_name = 'units'
    template_name = 'admin/unit_list.html'
    permission_required = 'main.view_unit'
