
from rest_framework import permissions
import logging

logger = logging.getLogger(__name__)

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    მხოლოდ ობიექტის მფლობელს აქვს წერის/განახლების უფლება.
    სხვებს აქვთ მხოლოდ წაკითხვის უფლება.
    """
    def has_object_permission(self, request, view, obj):
        logger.info(f"Checking permission for user: {request.user.username} (ID: {request.user.id if request.user.is_authenticated else 'N/A'}), is_authenticated: {request.user.is_authenticated}")
        logger.info(f"Request method: {request.method}")
        owner_username = obj.მფლობელი.username if obj.მფლობელი and hasattr(obj.მფლობელი, 'username') else 'None'
        owner_id = obj.მფლობელი.id if obj.მფლობელი and hasattr(obj.მფლობელი, 'id') else 'N/A'
        logger.info(f"Object owner: {owner_username} (ID: {owner_id})")

        # წაკითხვის უფლება ნებადართულია ნებისმიერი მოთხოვნის მეთოდისთვის.
        # GET, HEAD ან OPTIONS ყოველთვის ნებადართულია.
        if request.method in permissions.SAFE_METHODS:
            logger.info(f"Method {request.method} is SAFE_METHOD, allowing access.")
            return True

        if not request.user.is_authenticated:
            logger.warning("Attempt to modify object by unauthenticated user, denying access.")
            return False

        # წერის უფლება მხოლოდ ობიექტის მფლობელს აქვს.
        # დარწმუნდით, რომ ობიექტს აქვს 'მფლობელი' ატრიბუტი, რომელიც არის User მოდელი.
        is_owner = (obj.მფლობელი == request.user)
        logger.info(f"Is current user the owner? {is_owner}")
        return is_owner

class IsBookOwner(permissions.BasePermission):
    """
    მხოლოდ წიგნის მფლობელს აქვს წვდომა ამ ფუნქციაზე.
    გამოიყენება custom action-ებისთვის, როგორიცაა request-ების ნახვა ან მიღება/უარყოფა.
    """
    def has_object_permission(self, request, view, obj):
        # ობიექტი აქ არის Book instance
        if request.user.is_authenticated and obj.მფლობელი == request.user:
            return True
        return False