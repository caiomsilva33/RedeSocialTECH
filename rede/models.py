# redesocial/rede/models.py
from django.db import models
from django.contrib.auth.models import User
# from django.utils import timezone # Já estava importado, mas não é usado diretamente aqui agora

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    area_tecnologia = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    autor = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='posts')
    texto = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post de {self.autor.user.username} em {self.criado_em.strftime('%Y-%m-%d %H:%M:%S')}"

# NOVO MODELO ABAIXO
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    autor = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='comments')
    texto = models.TextField(max_length=500) # Limite de caracteres para comentários
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['criado_em'] # Ordena os comentários do mais antigo para o mais novo por padrão

    def __str__(self):
        return f'Comentário de {self.autor.user.username} em "{self.post.texto[:20]}..."'