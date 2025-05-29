# RedeSocialTECH

Bem-vindo à RedeSocialTECH! Este é um projeto de uma plataforma de rede social temática para entusiastas e profissionais de tecnologia, desenvolvida com Python e Django.

## Descrição

Esta aplicação permite que usuários se registrem, criem perfis, postem atualizações, comentem nas postagens de outros, curtam posts e visualizem perfis de outros membros da comunidade. O foco é criar um espaço para discussões e compartilhamento de conhecimento na área de tecnologia.

## Funcionalidades Implementadas

Com base no que desenvolvemos juntos:

* **Autenticação de Usuários:**
    * Registro de novas contas
    * Login e Logout de usuários
* **Perfis de Usuário:**
    * Criação automática de perfil (via `get_or_create` ou signals, se implementado)
    * Visualização do próprio perfil ("Meu Perfil")
    * Edição de informações do perfil (Biografia, Área de Tecnologia)
    * Visualização do perfil público de outros usuários (ex: `/perfil/username/`)
* **Posts:**
    * Criação de novas postagens de texto
    * Visualização de posts em um feed cronológico principal
    * Listagem de posts na página de perfil do usuário
    * Edição de posts próprios
    * Exclusão de posts próprios (com confirmação)
* **Interação Social:**
    * Adicionar comentários a posts
    * Visualizar comentários existentes abaixo dos posts
    * Curtir e Descurtir posts
    * Visualização da contagem de curtidas
* **Interface e UX:**
    * Design responsivo básico com tema escuro e cores personalizadas.
    * Feedback ao usuário através do sistema de mensagens do Django após ações.
    * Navegação padronizada entre as páginas.

## Tecnologias Utilizadas

* **Backend:** Python 3.13 (ou a versão que você está usando), Django 5.2 (ou a versão que você está usando)
* **Frontend:** HTML5, CSS3 (sem frameworks JavaScript principais até o momento)
* **Banco de Dados:** SQLite (padrão do Django para desenvolvimento)
* **Controle de Versão:** Git e GitHub

## Configuração e Instalação Local

Siga estas instruções para rodar o projeto localmente na sua máquina.

### Pré-requisitos

* Python (versão 3.8 ou superior - idealmente a que você usou no desenvolvimento, ex: 3.13.3)
* pip (gerenciador de pacotes do Python)
* Git

### Passos para Instalação

1.  **Clone o Repositório:**
    ```bash
    git clone [https://github.com/caiomsilva33/RedeSocialTECH.git](https://github.com/caiomsilva33/RedeSocialTECH.git)
    cd RedeSocialTECH
    ```

2.  **Crie e Ative um Ambiente Virtual (Altamente Recomendado):**
    ```bash
    python -m venv venv
    ```
    * No Windows:
        ```bash
        venv\Scripts\activate
        ```
    * No macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

3.  **Instale as Dependências:**
    Primeiro, certifique-se de que você tem um arquivo `requirements.txt` no seu repositório. Se não tiver, crie-o (com seu ambiente virtual ativado):
    ```bash
    pip freeze > requirements.txt
    ```
    Depois, adicione este arquivo ao Git (`git add requirements.txt`, `git commit -m "Adiciona requirements.txt"`, `git push`).
    Para instalar as dependências:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Aplique as Migrações do Banco de Dados:**
    ```bash
    python manage.py migrate
    ```

5.  **Crie um Superusuário (Opcional, para acesso ao Admin Django):**
    ```bash
    python manage.py createsuperuser
    ```
    Siga as instruções para definir nome de usuário, email e senha.

6.  **Rode o Servidor de Desenvolvimento:**
    ```bash
    python manage.py runserver
    ```
    A aplicação estará acessível em `http://127.0.0.1:8000/`.

## Como Usar

1.  Acesse `http://127.0.0.1:8000/`.
2.  **Registre-se** para uma nova conta ou faça **Login** se já tiver uma.
3.  Explore o **Feed**, crie **Novos Posts**.
4.  Visite **Meu Perfil** para editar suas informações.
5.  Interaja com posts: **Curta** e **Comente**.
6.  Clique nos nomes dos autores para ver os **Perfis de Outros Usuários**.
