# redesocial/rede/models.py
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings # Para a URL do avatar/capa padrão via static
from django.templatetags.static import static as staticfiles_tag # Para construir URL estática

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    area_tecnologia = models.CharField(max_length=100, blank=True, null=True)
    avatar = models.ImageField(
        upload_to='avatars/',
        null=True, 
        blank=True, 
        default='avatars/default_avatar.png' # Este caminho é relativo a MEDIA_ROOT
    )
    cover_photo = models.ImageField(
        upload_to='covers/',
        null=True,
        blank=True,
        default='covers/default_cover.png' # Este caminho é relativo a MEDIA_ROOT
    )
    following = models.ManyToManyField(
        'self', 
        related_name='followers', 
        symmetrical=False, 
        blank=True
    )

    def __str__(self):
        return self.user.username

    @property
    def avatar_url_display(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        # Se o default no ImageField estiver configurado corretamente e o arquivo existir em media/avatars/default_avatar.png
        # o Django deve servir settings.MEDIA_URL + 'avatars/default_avatar.png' automaticamente
        # quando self.avatar.url é acessado e o campo avatar está vazio mas tem um default.
        # Caso contrário, você pode querer um fallback para um arquivo em static:
        # return staticfiles_tag('rede/images/default_avatar.png') # Exemplo se default estiver em static
        # Ou, se o default no ImageField já aponta para um arquivo em MEDIA_ROOT:
        try:
            # Tenta acessar a url que o default do ImageField forneceria
            return UserProfile._meta.get_field('avatar').get_default() if not self.avatar else self.avatar.url
        except: # Fallback muito genérico, idealmente trate exceções específicas
            return settings.STATIC_URL + 'rede/images/placeholder_avatar.png' # Tenha um placeholder em static

    @property
    def cover_photo_url_display(self):
        if self.cover_photo and hasattr(self.cover_photo, 'url'):
            return self.cover_photo.url
        try:
            return UserProfile._meta.get_field('cover_photo').get_default() if not self.cover_photo else self.cover_photo.url
        except:
            return settings.STATIC_URL + 'rede/images/placeholder_cover.png' # Tenha um placeholder em static

    def count_following(self):
        return self.following.count()

    def count_followers(self):
        return self.followers.count()

class Post(models.Model):
    autor = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='posts')
    texto = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)
    curtidas = models.ManyToManyField(User, related_name='posts_curtidos', blank=True)

    def __str__(self):
        return f"Post de {self.autor.user.username} em {self.criado_em.strftime('%Y-%m-%d %H:%M:%S')}"

    def total_curtidas(self):
        return self.curtidas.count()

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    autor = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='comments_feitos')
    texto = models.TextField(max_length=500)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['criado_em']

    def __str__(self):
        return f'Comentário de {self.autor.user.username} em "{self.post.texto[:20]}..."'