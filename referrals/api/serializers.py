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
            "password",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = Company(
            email=validated_data["email"],
            company_name=validated_data["company_name"],
            address=validated_data.get("address", ""),
            phone_no=validated_data.get("phone_no", ""),
            country=validated_data.get("country", ""),
            company_registration_no=validated_data["company_registration_no"],
            user_type="company",
        )
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
            "password",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = Individual(
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            gender=validated_data["gender"],
            phone_no=validated_data["phone_no"],
            address=validated_data.get("address", ""),
            country=validated_data.get("country", ""),
            state=validated_data["state"],
            city=validated_data["city"],
            user_type="individual",
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
