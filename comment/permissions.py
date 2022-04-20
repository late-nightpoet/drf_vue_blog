from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):

    message = 'You must be the owner to update'

    # def has_permission(self, request, view):
    #     if request.method in SAFE_METHODS:
    #         return True
    #
    #     return request.user.is_authenticated
    # 此方法早于 def perform_create(...) 执行，因此能够对用户登录状态做一个预先检查
    # def has_object_permission(self, request, view, obj):
    #     if request.method in SAFE_METHODS:
    #         return True
    #
    #     return obj.author == request.user
    # 晚于视图集中的 def perform_create(author=self.request.user) 执行的。如果用户未登录时新建评论，由于用户不存在，接口会抛出 500 错误。
    # 把重复代码集合出来
    def safe_methods_or_owner(self, request, func):
        if request.method in SAFE_METHODS:
            return True

        return func()

    def has_permission(self, request, view):
        return self.safe_methods_or_owner(
            request,
            lambda: request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return self.safe_methods_or_owner(
            request,
            lambda: obj.author == request.user
        )

