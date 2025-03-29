from rest_framework.permissions import BasePermission

class IsAcademyPermissions(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_academy)
    

class IsTeacherPermissions(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_teacher)
    

class IsTutorPermissions(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.is_authenticated and request.user.is_tutor)