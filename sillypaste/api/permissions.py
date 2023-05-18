from rest_framework.permissions import (
    SAFE_METHODS,
    BasePermission,
    IsAuthenticated,
)


class DenyAll(BasePermission):
    message = 'Not allowed at all'

    def has_permission(self, request, view):
        return False


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsSameUser(BasePermission):
    """Use on views with the queryset of User.objects"""

    message = 'Must be same user'

    def has_permission(self, request, view):
        return (
            IsAuthenticated().has_permission(request, view)
            and int(view.kwargs['pk']) == request.user.id
        )


class IsOwnerOrReadOnly(BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.author == request.user
