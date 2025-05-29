# redesocial/rede/models.py
from django.db import models
from django.contrib.auth.models import User

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
    curtidas = models.ManyToManyField(User, related_name='posts_curtidos', blank=True) # Campo para curtidas

    def __str__(self):
        return f"Post de {self.autor.user.username} em {self.criado_em.strftime('%Y-%m-%d %H:%M:%S')}"

    def total_curtidas(self):
        return self.curtidas.count()

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    autor = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='comments_feitos') # related_name ajustado
    texto = models.TextField(max_length=500)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['criado_em']

    def __str__(self):
        return f'Comentário de {self.autor.user.username} em "{self.post.texto[:20]}..."'