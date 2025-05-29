import os
import django
import sys

# Garante que o diretório raiz do projeto esteja no caminho de busca de módulos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

# Configura o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'redesocial.settings')
django.setup()

from django.contrib.auth.models import User
from rede.models import UserProfile

print("Iniciando a verificação e criação de perfis para usuários existentes...")

user_target_username = None # Deixa como None para processar todos os usuários sem perfil
# user_target_username = 'seu_nome_de_usuario' # <--- Descomente e mude aqui se quiser um específico

if user_target_username:
    try:
        users_to_process = [User.objects.get(username=user_target_username)]
        print(f"Processando perfil para o usuário: {user_target_username}")
    except User.DoesNotExist:
        print(f"Erro: Usuário '{user_target_username}' não encontrado. Verifique o nome de usuário.")
        users_to_process = []
else:
    # ATENÇÃO AQUI: Mude 'userprofile' para 'profile' devido ao related_name no models.py
    users_to_process = User.objects.filter(profile__isnull=True)
    print(f"Encontrados {users_to_process.count()} usuários sem perfil.")


for user in users_to_process:
    try:
        # Tenta criar o UserProfile para o usuário
        UserProfile.objects.create(user=user, bio='Minha biografia padrão', area_tecnologia='Tecnologia')
        print(f"UserProfile criado com sucesso para: {user.username}")
    except Exception as e:
        print(f"Erro ao criar UserProfile para {user.username}: {e}")

print("\nProcesso de verificação e criação de perfis concluído.")