from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Usuário ou senha incorretos.')
    return render(request, 'usuarios/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def lista_usuarios(request):
    if not request.user.is_superuser:
        messages.error(request, 'Acesso restrito ao administrador.')
        return redirect('dashboard')
    usuarios = User.objects.all().order_by('first_name', 'username')
    return render(request, 'usuarios/lista.html', {'usuarios': usuarios})


@login_required
def novo_usuario(request):
    if not request.user.is_superuser:
        messages.error(request, 'Acesso restrito ao administrador.')
        return redirect('dashboard')
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        is_superuser = request.POST.get('is_superuser') == 'on'

        if User.objects.filter(username=username).exists():
            messages.error(request, f'O usuário "{username}" já existe.')
            return render(request, 'usuarios/form.html', {'acao': 'Novo'})

        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_superuser=is_superuser,
            is_staff=is_superuser,
        )
        messages.success(request, f'Usuário "{user.get_full_name() or user.username}" criado com sucesso!')
        return redirect('lista_usuarios')

    return render(request, 'usuarios/form.html', {'acao': 'Novo'})


@login_required
def editar_usuario(request, pk):
    if not request.user.is_superuser:
        messages.error(request, 'Acesso restrito ao administrador.')
        return redirect('dashboard')

    usuario = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        usuario.first_name = request.POST.get('first_name', '').strip()
        usuario.last_name = request.POST.get('last_name', '').strip()
        usuario.is_superuser = request.POST.get('is_superuser') == 'on'
        usuario.is_staff = usuario.is_superuser
        usuario.is_active = request.POST.get('is_active') == 'on'

        nova_senha = request.POST.get('password', '').strip()
        if nova_senha:
            usuario.set_password(nova_senha)

        usuario.save()
        messages.success(request, f'Usuário "{usuario.get_full_name() or usuario.username}" atualizado!')
        return redirect('lista_usuarios')

    return render(request, 'usuarios/form.html', {'acao': 'Editar', 'usuario': usuario})


@login_required
def trocar_senha(request):
    """Qualquer usuário pode trocar a própria senha."""
    if request.method == 'POST':
        senha_atual = request.POST.get('senha_atual', '')
        nova_senha = request.POST.get('nova_senha', '').strip()
        confirmar = request.POST.get('confirmar', '').strip()

        if not request.user.check_password(senha_atual):
            messages.error(request, 'Senha atual incorreta.')
        elif nova_senha != confirmar:
            messages.error(request, 'As senhas não coincidem.')
        elif len(nova_senha) < 4:
            messages.error(request, 'A nova senha deve ter pelo menos 4 caracteres.')
        else:
            request.user.set_password(nova_senha)
            request.user.save()
            login(request, request.user)
            messages.success(request, 'Senha alterada com sucesso!')
            return redirect('dashboard')

    return render(request, 'usuarios/trocar_senha.html')
