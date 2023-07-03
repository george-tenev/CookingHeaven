from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from CookingHeaven.common.view_mixins import AdminRequiredMixin


class AdminPanelView(LoginRequiredMixin, AdminRequiredMixin, TemplateView):
    template_name = "admin/admin_panel.html"
