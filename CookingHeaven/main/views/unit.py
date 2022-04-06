from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Permission
from django.urls import reverse_lazy
from django.views.generic import CreateView

from CookingHeaven.common.view_mixins import AdminPermissionsRequiredMixin
from CookingHeaven.main.forms import UnitCreateForm
from CookingHeaven.main.models import Unit


class UnitCreateView(LoginRequiredMixin, AdminPermissionsRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Unit
    form_class = UnitCreateForm
    template_name = 'admin/unit_create.html'
    success_url = reverse_lazy('dashboard')
    permission_required = 'main.add_unit'