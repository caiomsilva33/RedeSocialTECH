# redesocial/rede/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages # Para exibir mensagens ao usuário (opcional, mas bom para erros de formulário)

# Importe todos os formulários e modelos necessários
from .forms import UserProfileForm, PostForm, RegistroForm, CommentForm
from .models import Post, UserProfile, Comment

@login_required
def feed(request):
    posts = Post.objects.all().order_by('-criado_em')
    comment_form = CommentForm()
    
    context = {
        'posts': posts,
        'comment_form': comment_form,
    }
    return render(request, 'rede/feed.html', context)

@login_required
def novo_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            # Garante que o UserProfile exista para o autor
            user_profile, created = UserProfile.objects.get_or_create(user=request.user)
            post.autor = user_profile
            post.save()
            return redirect('feed')
    else:
        form = PostForm()
    return render(request, 'rede/novo_post.html', {'form': form})

@login_required
def perfil(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    user_posts = Post.objects.filter(autor=user_profile).order_by('-criado_em')
    
    # Formulário para editar o perfil
    if request.method == 'POST' and 'update_profile_submit' in request.POST:
        # Este bloco é para quando o formulário de edição de perfil é submetido
        profile_edit_form_instance = UserProfileForm(request.POST, instance=user_profile)
        if profile_edit_form_instance.is_valid():
            profile_edit_form_instance.save()
            messages.success(request, 'Seu perfil foi atualizado com sucesso!')
            return redirect('perfil')
        else:
            messages.error(request, 'Não foi possível atualizar seu perfil. Verifique os erros abaixo.')
            # Se o formulário de edição de perfil tiver erros, queremos re-renderizar a página
            # com este formulário preenchido com erros.
            # O comment_form será uma nova instância vazia.
            comment_form_instance = CommentForm()
    else:
        # Requisição GET ou POST de outro formulário (o de comentário é tratado por add_comment)
        profile_edit_form_instance = UserProfileForm(instance=user_profile)
        comment_form_instance = CommentForm()

    # Garante que comment_form_instance seja definido mesmo se o POST do perfil falhar
    if 'comment_form_instance' not in locals():
        comment_form_instance = CommentForm()
        
    context = {
        'profile_edit_form': profile_edit_form_instance,
        'user_profile': user_profile,
        'posts': user_posts,
        'comment_form': comment_form_instance,
    }
    return render(request, 'rede/perfil.html', context)

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            # UserProfile é criado automaticamente via signal (assumindo que você o tem configurado)
            login(request, user)
            messages.success(request, f'Bem-vindo(a), {user.username}! Seu registro foi concluído com sucesso.')
            return redirect('feed')
        else:
            messages.error(request, 'Não foi possível criar sua conta. Por favor, corrija os erros abaixo.')
    else:
        form = RegistroForm()
    return render(request, 'rede/registro.html', {'form': form})

@login_required
def editar_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.autor != request.user.profile:
        return HttpResponseForbidden("Você não tem permissão para editar este post.")

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post atualizado com sucesso!')
            # Redireciona para o feed com âncora para o post editado
            return HttpResponseRedirect(reverse('feed') + f'#post-{post.id}')
    else:
        form = PostForm(instance=post)

    return render(request, 'rede/editar_post.html', {'form': form, 'post': post})

@login_required
def apagar_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.autor != request.user.profile:
        return HttpResponseForbidden("Você não tem permissão para apagar este post.")

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post apagado com sucesso.')
        return redirect('feed')

    return render(request, 'rede/apagar_post_confirmar.html', {'post': post})

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    # Determina para onde redirecionar: usa 'next' se fornecido, senão o feed com âncora.
    next_url_base = request.POST.get('next', reverse('feed'))
    anchor = f'#post-{post.id}'
    
    # Constrói a URL de redirecionamento final
    # Se next_url_base já for uma URL completa (ex: de request.path), apenas adicionamos a âncora
    # Se for um nome de URL (como 'feed' ou 'perfil'), reverse() é necessário.
    # A lógica aqui assume que 'next' pode ser um path ou um nome de url que precisa ser revertido
    # Para simplificar, se 'next' for passado, ele já deve ser um path válido.
    if request.POST.get('next'): # Se o campo 'next' foi enviado pelo formulário
        redirect_target_url = f"{request.POST.get('next')}{anchor}"
    else: # Senão, redireciona para o feed
        redirect_target_url = f"{reverse('feed')}{anchor}"

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            user_profile, created = UserProfile.objects.get_or_create(user=request.user)
            comment.autor = user_profile
            comment.save()
            messages.success(request, 'Seu comentário foi adicionado!')
            return HttpResponseRedirect(redirect_target_url)
        else:
            # Se o formulário de comentário for inválido
            messages.error(request, 'Não foi possível adicionar seu comentário. Verifique o texto.')
            # Redireciona de volta para a página de origem (com a âncora)
            # Isso não vai exibir os erros do formulário na página de origem,
            # apenas a mensagem de erro geral. Para exibir erros de campo,
            # a lógica de renderização da página de origem (feed/perfil) precisaria ser mais complexa.
            return HttpResponseRedirect(redirect_target_url) 
    else:
        # Não deve ser acessado via GET para adicionar comentário
        return redirect('feed')