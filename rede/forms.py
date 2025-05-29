# redesocial/rede/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Post, Comment

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'area_tecnologia']
        widgets = {
            'bio': forms.Textarea(attrs={'placeholder': 'Descreva-se em poucas palavras...'}),
            'area_tecnologia': forms.TextInput(attrs={'placeholder': 'Ex: Python, Frontend, DevOps'})
        }
        labels = {
            'bio': 'Biografia',
            'area_tecnologia': 'Área de Tecnologia',
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['texto']
        widgets = {
            'texto': forms.Textarea(attrs={'rows': 5, 'placeholder': 'O que você está pensando agora?'})
        }
        labels = {
            'texto': 'Seu post:'
        }

class RegistroForm(UserCreationForm):
    email = forms.EmailField(label="Endereço de e-mail", required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Nome de usuário"
        self.fields['username'].help_text = 'Obrigatório. 150 caracteres ou menos. Letras, dígitos e @/./+/-/_ apenas.'
        
        if 'password' in self.fields:
            self.fields['password'].label = "Senha"
        
        if 'password2' in self.fields:
            self.fields['password2'].label = "Confirmação de senha"
            self.fields['password2'].help_text = 'Digite a mesma senha informada acima, para verificação.'

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['texto']
        widgets = {
            'texto': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Adicione um comentário...',
                'class': 'form-control comment-textarea'
            })
        }
        labels = {
            'texto': '' # Oculta o label "Texto:"
        }