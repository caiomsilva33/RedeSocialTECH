# Arquivo: redesocial/rede/views.py
# Por favor, substitua todo o conteúdo do seu arquivo views.py por este.

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.models import User 
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

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
            user_profile, created = UserProfile.objects.get_or_create(user=request.user)
            post.autor = user_profile
            post.save()
            messages.success(request, 'Seu post foi criado com sucesso!')
            return redirect('feed')
        else:
            messages.error(request, 'Não foi possível criar seu post. Verifique os erros abaixo.')
    else:
        form = PostForm()
    return render(request, 'rede/novo_post.html', {'form': form})

@login_required
def perfil(request): # View para o perfil do usuário logado (name='meu_perfil')
    user_profile_obj, created = UserProfile.objects.get_or_create(user=request.user)
    user_posts = Post.objects.filter(autor=user_profile_obj).order_by('-criado_em')
    
    profile_edit_form_instance = UserProfileForm(instance=user_profile_obj)
    comment_form_instance = CommentForm()

    if request.method == 'POST':
        if 'update_profile_submit' in request.POST:
            profile_edit_form_instance = UserProfileForm(request.POST, request.FILES or None, instance=user_profile_obj)
            if profile_edit_form_instance.is_valid():
                profile_edit_form_instance.save()
                messages.success(request, 'Seu perfil foi atualizado com sucesso!')
                return redirect('meu_perfil')
            else:
                messages.error(request, 'Não foi possível atualizar seu perfil. Verifique os erros abaixo.')
        
    context = {
        'profile_user': user_profile_obj,
        'profile_edit_form': profile_edit_form_instance,
        'posts': user_posts,
        'comment_form': comment_form_instance,
        'is_own_profile': True 
    }
    return render(request, 'rede/perfil.html', context)

# ESTA É A VIEW QUE ESTAVA CAUSANDO O AttributeError ANTERIORMENTE
# Certifique-se que ela está presente e correta.
@login_required 
def user_profile_view(request, username): # View para perfis de outros usuários (name='user_profile')
    profile_owner_user = get_object_or_404(User, username=username)
    user_profile_obj = get_object_or_404(UserProfile, user=profile_owner_user)
    
    user_posts = Post.objects.filter(autor=user_profile_obj).order_by('-criado_em')
    comment_form_instance = CommentForm()
    is_own_profile = (request.user == profile_owner_user)

    if is_own_profile:
        return redirect('meu_perfil') # Redireciona para a view 'perfil' se for o próprio usuário

    context = {
        'profile_user': user_profile_obj, 
        'posts': user_posts,
        'comment_form': comment_form_instance,
        'is_own_profile': is_own_profile, 
    }
    return render(request, 'rede/perfil.html', context)


def registro(request):
    if request.user.is_authenticated:
        return redirect('feed')
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
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
    # Corrigido para verificar o 'user' dentro do 'autor' UserProfile
    if post.autor.user != request.user: 
        return HttpResponseForbidden("Você não tem permissão para editar este post.")

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post atualizado com sucesso!')
            return HttpResponseRedirect(reverse('feed') + f'#post-{post.id}')
        else:
            messages.error(request, 'Não foi possível atualizar o post. Verifique os erros abaixo.')
    else:
        form = PostForm(instance=post)
    return render(request, 'rede/editar_post.html', {'form': form, 'post': post})

@login_required
def apagar_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    # Corrigido para verificar o 'user' dentro do 'autor' UserProfile
    if post.autor.user != request.user: 
        return HttpResponseForbidden("Você não tem permissão para apagar este post.")

    if request.method == 'POST':
        post_autor_username = post.autor.user.username
        post.delete()
        messages.success(request, f'Post de {post_autor_username} apagado com sucesso.')
        return redirect('feed')
    return render(request, 'rede/apagar_post_confirmar.html', {'post': post})

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    next_url_from_form = request.POST.get('next', '')
    anchor = f'#post-{post.id}'
    redirect_target_url = f"{reverse('feed')}{anchor}"

    if next_url_from_form:
        if anchor in next_url_from_form:
            redirect_target_url = next_url_from_form
        else:
            redirect_target_url = f"{next_url_from_form}{anchor}"
            
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
            error_message = "Não foi possível adicionar seu comentário."
            if 'texto' in form.errors:
                error_message += f" Detalhe: {form.errors['texto'][0]}"
            messages.error(request, error_message)
            return HttpResponseRedirect(redirect_target_url) 
    else:
        return redirect('feed')

@login_required
def like_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    next_url_from_form = request.POST.get('next', '')
    anchor = f'#post-{post.id}'
    redirect_target_url = f"{reverse('feed')}{anchor}" 
    
    if next_url_from_form:
        if anchor in next_url_from_form:
            redirect_target_url = next_url_from_form
        else:
            redirect_target_url = f"{next_url_from_form}{anchor}"

    if request.method == 'POST':
        if request.user in post.curtidas.all():
            post.curtidas.remove(request.user)
        else:
            post.curtidas.add(request.user)
        return HttpResponseRedirect(redirect_target_url)
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('feed')))