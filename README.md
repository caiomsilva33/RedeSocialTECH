# Rede Social Tech (Sugestão de Nome)

Bem-vindo à Rede Social Tech! Este é um projeto de uma plataforma de rede social temática para entusiastas e profissionais de tecnologia, desenvolvida com Python e Django.

## Descrição

Esta aplicação permite que usuários se registrem, criem perfis, postem atualizações, comentem nas postagens de outros, curtam posts e visualizem perfis de outros membros da comunidade. O foco é criar um espaço para discussões e compartilhamento de conhecimento na área de tecnologia.

## Funcionalidades Implementadas

* **Autenticação de Usuários:**
    * Registro de novas contas
    * Login e Logout de usuários
* **Perfis de Usuário:**
    * Criação automática de perfil ao registrar
    * Visualização do próprio perfil ("Meu Perfil")
    * Edição de informações do perfil (Biografia, Área de Tecnologia)
    * Visualização do perfil público de outros usuários
* **Posts:**
    * Criação de novas postagens de texto
    * Visualização de posts em um feed cronológico
    * Edição de posts próprios
    * Exclusão de posts próprios
* **Interação com Posts:**
    * Adicionar comentários a posts
    * Visualizar comentários existentes
    * Curtir e Descurtir posts
    * Visualização da contagem de curtidas
* **Interface e UX:**
    * Design responsivo básico com tema escuro
    * Feedback ao usuário através do sistema de mensagens do Django

## Tecnologias Utilizadas

* **Backend:** Python, Django
* **Frontend:** HTML, CSS (sem frameworks JavaScript complexos até o momento)
* **Banco de Dados:** SQLite (padrão do Django para desenvolvimento)

## Configuração e Instalação Local

Siga estas instruções para rodar o projeto localmente na sua máquina.

### Pré-requisitos

* Python 3.8 ou superior (Recomendado: A versão que você está utilizando, ex: 3.13)
* pip (gerenciador de pacotes do Python)
* Git (para clonar o repositório, se aplicável)

### Passos para Instalação

1.  **Clone o Repositório (se estiver no GitHub):**
    ```bash
    git clone [https://github.com/SEU_USUARIO/NOME_DO_SEU_REPOSITORIO.git](https://github.com/SEU_USUARIO/NOME_DO_SEU_REPOSITORIO.git)
    cd NOME_DO_SEU_REPOSITORIO
    ```
    Se você já tem o projeto localmente, pule este passo.

2.  **Crie e Ative um Ambiente Virtual (Recomendado):**
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
    Primeiro, você precisa criar um arquivo `requirements.txt` se ainda não tiver um. Com seu ambiente virtual ativado, na pasta raiz do projeto, rode:
    ```bash
    pip freeze > requirements.txt
    ```
    Este comando listará todas as dependências do seu projeto (como Django) no arquivo. Depois disso (ou se o arquivo já existir no repositório clonado), instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Aplique as Migrações do Banco de Dados:**
    Este comando cria as tabelas no seu banco de dados com base nos modelos definidos.
    ```bash
    python manage.py migrate
    ```

5.  **Crie um Superusuário (Opcional, para acesso ao Admin):**
    Isso permite que você acesse a interface de administração do Django.
    ```bash
    python manage.py createsuperuser
    ```
    Siga as instruções para definir nome de usuário, email e senha.

6.  **Rode o Servidor de Desenvolvimento:**
    ```bash
    python manage.py runserver
    ```
    Por padrão, a aplicação estará acessível em `http://127.0.0.1:8000/` no seu navegador.

## Como Usar (Principais Fluxos)

1.  **Registre-se:** Crie uma nova conta para começar.
2.  **Faça Login:** Acesse sua conta.
3.  **Edite seu Perfil:** Vá em "Meu Perfil" para adicionar sua bio e área de tecnologia.
4.  **Crie Posts:** Compartilhe suas ideias e conhecimentos.
5.  **Interaja:** Navegue pelo feed, curta posts e deixe comentários.
6.  **Veja Perfis:** Clique no nome de outros usuários para ver seus perfis e posts.

## Futuras Melhorias (Sugestões)

* [ ] Implementar sistema de "Seguir Usuários"
* [ ] Adicionar upload de imagens para posts e fotos de perfil/capa
* [ ] Notificações em tempo real (ou periódicas)
* [ ] Mensagens diretas entre usuários
* [ ] Pesquisa de posts e usuários
* [ ] Paginação para o feed e listas de posts/comentários
* [ ] Testes automatizados

## Contribuição

Se você gostaria de contribuir com este projeto, por favor, sinta-se à vontade para... (Explique como você gostaria que as contribuições fossem feitas, ex: abrindo issues, enviando pull requests, etc. Se for um projeto pessoal, você pode omitir esta seção ou dizer que não está aceitando contribuições no momento).

## Licença

(Se você quiser adicionar uma licença, como a MIT License, coloque aqui. Por exemplo: Este projeto está licenciado sob a Licença MIT - veja o arquivo `LICENSE.md` para detalhes.)
Se você não tiver um arquivo `LICENSE.md`, pode omitir esta seção ou escolher uma licença.

---

Lembre-se de substituir `(Sugestão de Nome)`, `SEU_USUARIO` e `NOME_DO_SEU_REPOSITORIO` pelos nomes corretos.

**Dicas Adicionais para o GitHub:**

* **`.gitignore`**: Certifique-se de ter um arquivo `.gitignore` na raiz do seu projeto para evitar que arquivos desnecessários ou sensíveis (como `db.sqlite3`, a pasta `venv/`, arquivos `__pycache__/`, etc.) sejam enviados para o GitHub. Um bom `.gitignore` para projetos Django pode ser encontrado online (o GitHub geralmente sugere um ao criar um novo repositório para Python).
    Exemplo de conteúdo básico para `.gitignore`:
    ```
    # Ambientes Virtuais
    venv/
    env/
    *.pyc
    __pycache__/
    db.sqlite3
    ```
