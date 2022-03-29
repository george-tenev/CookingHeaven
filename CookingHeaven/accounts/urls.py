from django.urls import path, include

from CookingHeaven.accounts import views

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('delete/<int:pk>', views.UserDeleteView.as_view(), name='delete'),

    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path("password_change/", views.PasswordChangeView.as_view(), name="password_change"),

    path('admin_profile_create/', views.AdminCreateProfileView.as_view(), name='admin profile create'),

    path('update/<int:pk>/', views.ProfileUpdateView.as_view(), name='profile update'),
    path('details/<int:pk>/', views.ProfileDetailsView.as_view(), name='profile details'),
]