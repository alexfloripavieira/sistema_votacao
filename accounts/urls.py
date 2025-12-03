from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('create-conselheiro/', views.CreateConselheiroView.as_view(), name='create_conselheiro'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('pending-users/', views.PendingPasswordChangeView.as_view(), name='pending_users'),
]
