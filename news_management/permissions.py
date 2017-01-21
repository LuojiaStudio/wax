from rest_framework import permissions


class IsNewsEditor(permissions.BasePermission):
    """
    can change all article
    """

    def has_permission(self, request, view):
        return request.user.has_perm('news_management.delete_article')