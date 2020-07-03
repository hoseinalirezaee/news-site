from rest_framework import permissions


class CanPost(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        f = user.has_perm('db.add_post')
        return f
