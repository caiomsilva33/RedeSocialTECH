# redesocial/redesocial/urls.py

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

# Imports necessários para servir arquivos de mídia em desenvolvimento
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'), # Considerar redirecionar para 'feed' ou outra página após logout
    path('', include('rede.urls')), # Suas URLs do app 'rede'
    path('accounts/', include('django.contrib.auth.urls')), # URLs de autenticação padrão do Django
]

# Adiciona as URLs para servir arquivos de mídia em modo de desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)