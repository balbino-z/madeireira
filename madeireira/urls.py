from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponseRedirect
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),  # Tela de login
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Logout
    path('pedidos/', include('core.urls')),  # Rotas do app core
]