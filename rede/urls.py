# redesocial/rede/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.feed, name='feed'),
    path('novo_post/', views.novo_post, name='novo_post'),
    path('perfil/', views.perfil, name='meu_perfil'),
    path('perfil/<str:username>/', views.user_profile_view, name='user_profile'),
    path('registro/', views.registro, name='registro'),
    path('post/<int:post_id>/editar/', views.editar_post, name='editar_post'),
    path('post/<int:post_id>/apagar/', views.apagar_post, name='apagar_post'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('post/<int:post_id>/like/', views.like_post_view, name='like_post'),
    path('usuarios/pesquisa/', views.user_search_results_view, name='user_search_results'),
    
    # NOVAS URLs para seguir/deixar de seguir
    path('perfil/<str:username>/follow/', views.follow_user_view, name='follow_user'),
    path('perfil/<str:username>/unfollow/', views.unfollow_user_view, name='unfollow_user'),
]