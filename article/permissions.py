from rest_framework import permissions


class IsAdminUserOrReadOnly(permissions.BasePermission):
    '''
    仅管理员用户可进行修改
    其他用户仅可查看
    '''
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        # 仅管理员可进行修改
        return request.user.is_superuser
