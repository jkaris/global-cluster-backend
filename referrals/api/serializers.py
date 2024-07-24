from rest_framework import serializers
from ..models import Company, Individual


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
        validated_data["user_type"] = "company"
        user = Individual(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    user_type = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
