from django.contrib.auth.mixins import UserPassesTestMixin


class SuperuserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class AdminPermissionsRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff