from rest_framework import serializers
from ..models import Company, Individual, Product, SupportTicket, UserRanking, CustomUser, UserRegistration, \
    BusinessRegistration, ProductImage


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = (
            "company_name",
            "email",
            "address",
            "phone_no",
            "country",
            "company_registration_no",
            "user_type",
            "password",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        validated_data["user_type"] = "company"
        user = Company(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class IndividualSerializer(serializers.ModelSerializer):
    class Meta:
        model = Individual
        fields = (
            "first_name",
            "last_name",
            "gender",
            "phone_no",
            "address",
            "country",
            "state",
            "city",
            "email",
            "user_type",
            "password",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        validated_data["user_type"] = "individual"
        user = Individual(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    user_type = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)


class UserDetailSerializer(serializers.ModelSerializer):
    company_details = CompanySerializer(source='company', read_only=True)
    individual_details = IndividualSerializer(source='individual', read_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'user_type', 'company_details', 'individual_details']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = "__all__"


class SupportTicketSerializer(serializers.ModelSerializer):
    submitted_by = serializers.ReadOnlyField(source="submitted_by.username")

    class Meta:
        model = SupportTicket
        fields = [
            "uuid",
            "date_created",
            "date_updated",
            "submitted_by",
            "support",
            "title",
            "description",
            "status",
            "priority",
            "attachments",
        ]
        read_only_fields = ["uuid", "date_created", "date_updated", "submitted_by"]


class UserRankingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRanking
        fields = "__all__"


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    user_type = serializers.ChoiceField(choices=['individual'], write_only=True)

    class Meta:
        model = UserRegistration
        fields = ['email', 'password', 'full_name', 'sponsor', 'user_type']
        extra_kwargs = {'sponsor': {'required': False}}

    def create(self, validated_data):
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        user_type = validated_data.pop('user_type')

        user = CustomUser.objects.create_user(email=email, password=password, user_type=user_type, sponsor=sponsor)
        user_registration = UserRegistration.objects.create(user=user, **validated_data)
        return user_registration


class BusinessRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    user_type = serializers.ChoiceField(choices=['company'], write_only=True)

    class Meta:
        model = BusinessRegistration
        fields = ['email', 'password', 'company_name', 'user_type']
        extra_kwargs = {'company_name': {'required': False}}

    def create(self, validated_data):
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        user_type = validated_data.pop('user_type')

        user = CustomUser.objects.create_user(email=email, password=password, user_type=user_type)
        business_registration = BusinessRegistration.objects.create(user=user, **validated_data)
        return business_registration
