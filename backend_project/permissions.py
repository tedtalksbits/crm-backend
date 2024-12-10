from rest_framework.permissions import BasePermission

class IsCompanyUser(BasePermission):
  def has_permission(self, request, view):
    user = request.user
    print(f'User: {user}')
    print(f'User: {user.is_superuser}')
    print(f'User: {user} Is Authenticated: {user.is_authenticated}')
    # Superuser bypass
    if user.is_superuser:
      return True
    
    if not user.is_authenticated or not user.company:
      return False
    # Check resource company
    resource_company = view.get_object().company
    return user.company == resource_company
