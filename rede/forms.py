# redesocial/rede/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Post, Comment # Certifique-se que UserProfile (o modelo) está importado

class UserProfileForm(forms.ModelForm): # <-- ESTA É A CLASSE QUE ESTÁ FALTANDO OU INCORRETA
    class Meta:
        model = UserProfile # O modelo UserProfile deve estar definido em models.py e importado
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
    email = forms.EmailField(label="Endereço de e-mail", required=True) # Adicionando e tornando obrigatório

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email") # Removido password1 e password2 dos fields diretos
                                       # UserCreationForm cuida dos campos de senha
        # labels e help_texts para username e email podem ser definidos aqui se necessário
        # ou no __init__ para mais controle.

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Nome de usuário"
        self.fields['username'].help_text = 'Obrigatório. 150 caracteres ou menos. Letras, dígitos e @/./+/-/_ apenas.'
        
        # UserCreationForm adiciona password1 e password2. Vamos ajustar seus labels.
        if 'password' in self.fields: # O campo é nomeado 'password' no formulário base UserCreationForm
            self.fields['password'].label = "Senha"
            # As ajudas de senha vêm dos validadores, LANGUAGE_CODE='pt-br' pode ajudar a traduzi-las.
        
        if 'password2' in self.fields:
            self.fields['password2'].label = "Confirmação de senha"
            self.fields['password2'].help_text = 'Digite a mesma senha informada acima, para verificação.'

# NOVO FORMULÁRIO ABAIXO
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['texto'] # Apenas o campo de texto será editável pelo usuário no formulário
        widgets = {
            'texto': forms.Textarea(attrs={
                'rows': 2, # Menor que o de posts
                'placeholder': 'Adicione um comentário...',
                'class': 'form-control comment-textarea' # Adicionaremos estilo para esta classe
            })
        }
        labels = {
            'texto': '' # Oculta o label "Texto:" se o placeholder for suficiente
        }
