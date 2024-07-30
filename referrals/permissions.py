from rest_framework.permissions import BasePermission


class IsCompanyOrAdmin(BasePermission):
    """
    Custom permission class to check if the user making the request is authenticated and has a user type of 'company'
    or 'admin'.
    """

    def has_permission(self, request, view):
        """
        Check if the user making the request is authenticated and has a user type of 'company' or 'admin'.

        Parameters:
            request (HttpRequest): The HTTP request object.
            view (View): The view object.

        Returns:
            bool: True if the user is authenticated and has a user type of 'company' or 'admin', False otherwise.
        """
        return (
            request.user
            and request.user.is_authenticated
            and request.user.user_type in ["company", "admin"]
        )
