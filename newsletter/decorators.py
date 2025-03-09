from django.core.exceptions import PermissionDenied
from functools import wraps


def user_owns_object(obj_attr):
    """ Декоратор для проверки, что пользователь управляет объектом. """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            obj = obj_attr(*args, **kwargs)
            if obj.user != request.user:
                raise PermissionDenied
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


# decorators.py

def manager_access(view_func):
    """ Декоратор, разрешающий доступ только менеджерам """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.groups.filter(name='Managers').exists():
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped_view
