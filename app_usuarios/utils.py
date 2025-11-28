from django.http import HttpResponseForbidden
from functools import wraps
from django.shortcuts import render, redirect, get_object_or_404

def tipo_required(*tipos_permitidos):
    """
    Restringe o acesso de acordo com o tipo de usuário.
    Aceita múltiplos tipos de usuários (exemplo: 'seguranca', 'aluno').
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                # Garante que o usuário esteja autenticado
                return redirect('login')

            perfil = getattr(request.user, 'perfil', None)
            if perfil is None or perfil.tipo not in tipos_permitidos:
                return HttpResponseForbidden("Acesso negado para este tipo de usuário.")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator