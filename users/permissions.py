from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsNotCorporate(BasePermission):
    message = ('У вас корпоративний акаунт.\
                 Зверніться до адміністратора для змінення даних профілю.')
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        else:
            return bool(request.user and request.user.is_authenticated
                        and not request.user.is_corporate_account)
