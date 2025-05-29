# Arquivo: redesocial/rede/views.py
# Código completo e atualizado

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.models import User 
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

# Importe todos os formulários e modelos necessários
from .forms import UserProfileForm, PostForm, RegistroForm, CommentForm
from .models import Post, UserProfile, Comment # UserProfile e User são cruciais aqui

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
def perfil(request): 
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

@login_required 
def user_profile_view(request, username): 
    profile_owner_user = get_object_or_404(User, username=username)
    # Garante que o UserProfile exista para o usuário do perfil visualizado
    user_profile_obj, created = UserProfile.objects.get_or_create(user=profile_owner_user)
    
    user_posts = Post.objects.filter(autor=user_profile_obj).order_by('-criado_em')
    comment_form_instance = CommentForm()
    is_own_profile = (request.user == profile_owner_user)

    if is_own_profile:
        return redirect('meu_perfil')

    # Verifica se o usuário logado já segue o perfil visualizado
    is_following = False
    if request.user.is_authenticated:
        current_user_profile, chup_created = UserProfile.objects.get_or_create(user=request.user)
        if user_profile_obj in current_user_profile.following.all():
            is_following = True

    context = {
        'profile_user': user_profile_obj, 
        'posts': user_posts,
        'comment_form': comment_form_instance,
        'is_own_profile': is_own_profile, 
        'is_following': is_following, # Passa o status de "seguindo" para o template
    }
    return render(request, 'rede/perfil.html', context)


def registro(request):
    if request.user.is_authenticated:
        return redirect('feed')
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            # UserProfile será criado via get_or_create na primeira vez que 'perfil' ou uma ação que precise dele for chamada.
            # Ou, se você tiver um signal post_save para User, ele seria criado lá.
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

@login_required 
def user_search_results_view(request):
    query = request.GET.get('q', '') 
    users_found = [] 
    if query:
        users_found = UserProfile.objects.filter(
            user__username__icontains=query
        ).select_related('user').order_by('user__username')
        if not users_found:
            messages.info(request, f"Nenhum usuário encontrado para '{query}'.")
    context = {
        'query': query,
        'users_found': users_found,
    }
    return render(request, 'rede/search_results.html', context)

# --- NOVAS VIEWS PARA SEGUIR/DEIXAR DE SEGUIR ---
@login_required
def follow_user_view(request, username):
    if request.method == 'POST':
        user_to_follow = get_object_or_404(User, username=username)
        current_user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        target_user_profile, created_target = UserProfile.objects.get_or_create(user=user_to_follow) # Garante que o perfil alvo exista

        if user_to_follow == request.user:
            messages.error(request, "Você não pode seguir a si mesmo.")
        elif target_user_profile not in current_user_profile.following.all():
            current_user_profile.following.add(target_user_profile)
            messages.success(request, f"Você agora está seguindo {username}.")
        else:
            messages.info(request, f"Você já está seguindo {username}.")
        return redirect('user_profile', username=username)
    else:
        # Requisições GET não são para esta ação
        return redirect('user_profile', username=username) # Ou para o feed

@login_required
def unfollow_user_view(request, username):
    if request.method == 'POST':
        user_to_unfollow = get_object_or_404(User, username=username)
        current_user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        target_user_profile, created_target = UserProfile.objects.get_or_create(user=user_to_unfollow)

        if user_to_unfollow == request.user:
            messages.error(request, "Você não pode deixar de seguir a si mesmo.")
        elif target_user_profile in current_user_profile.following.all():
            current_user_profile.following.remove(target_user_profile)
            messages.success(request, f"Você deixou de seguir {username}.")
        else:
            messages.info(request, f"Você não estava seguindo {username}.")
        return redirect('user_profile', username=username)
    else:
        # Requisições GET não são para esta ação
        return redirect('user_profile', username=username) # Ou para o feed