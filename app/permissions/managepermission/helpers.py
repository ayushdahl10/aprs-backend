from permissions.models import Permission
from django.contrib.auth.models import User
from permissions.models import Role


def check_user_permissions(user, request, method):
    if user.is_anonymous:
        role = Role.objects.get(name="AnonymousUser")
        permission_list = role.permissions.all()
        for permission in permission_list:
            if (
                permission.url_name == request
                and permission.url_type.lower() == str(method).lower()
            ):
                return True
    else:
        user = User.objects.get(email=user.email)
        user_groups = user.groups.all()
        if user.is_superuser:
            return True
        elif user.is_authenticated:
            for group in user_groups:
                role = Role.objects.get(name=group)
                permission_list = role.permissions.all()
                for permission in permission_list:
                    if (
                        permission.url_name.lower() == str(request).lower()
                        and permission.url_type.lower() == str(method).lower()
                    ):
                        return True

    return False
