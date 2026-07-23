from rest_framework.permissions import BasePermission
## My Custom Seller Check

class IsSeller(BasePermission):
    
    def has_permission(self, request, view):
        user = request.user
        print("IsSeller_1:", request, user)
        if not user or not request.user.is_authenticated:
            return False
        else:
            if user.user_type=="seller":
                return True

        return False
