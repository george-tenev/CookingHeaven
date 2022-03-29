from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from CookingHeaven.common.view_mixins import AdminPermissionsRequiredMixin
from CookingHeaven.main.models import FoodType


class FoodtypeCreateView(LoginRequiredMixin, AdminPermissionsRequiredMixin, CreateView):
    model = FoodType
    form_class = AdminPermissionsRequiredMixin
    template_name = 'main/product_create.html'
    success_url = reverse_lazy('dashboard')