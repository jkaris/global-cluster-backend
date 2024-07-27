from rest_framework import serializers
from .models import Product, SupportTicket


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model.
    """
    class Meta:
        model = Product
        fields = '__all__'

    def validate(self, data):
        """
        Validates the data provided in the request.

        This function checks if the request has a user attribute and if the user's user_type is either 'company' or
        'admin'. If not, it raises a serializers.ValidationError with the message "Only companies or admins can create
        products."

        Parameters:
            data (dict): The data to be validated.

        Returns:
            dict: The validated data.
        """
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
            if user.user_type not in ['company', 'admin']:
                raise serializers.ValidationError("Only companies or admins can create products.")
        return data


class SupportTicketSerializer(serializers.ModelSerializer):
    """
    Serializer for the SupportTicket model.
    """
    class Meta:
        model = SupportTicket
        fields = '__all__'

    def validate(self, data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
            if user.user_type not in ['individual', 'company']:
                raise serializers.ValidationError("Only individuals or companies can create support tickets.")
        return data
