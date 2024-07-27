from rest_framework import serializers
from .models import CustomUser, IndividualProfile, CompanyProfile


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'name', 'user_type', 'password', 'profile_picture']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)


class IndividualProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = IndividualProfile
        fields = ['first_name', 'last_name', 'gender', 'phone_number', 'address', 'country', 'state', 'city',
                  'user']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = CustomUser.objects.create_user(**user_data)
        individual_profile = IndividualProfile.objects.create(user=user, **validated_data)
        return individual_profile

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user = instance.user

        serializer = CustomUserSerializer(user, data=user_data, partial=True)
        if serializer.is_valid():
            serializer.save()
        instance = super().update(instance, validated_data)
        return instance


class CompanyProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = CompanyProfile
        fields = ['company_name', 'company_registration_number', 'phone_number', 'address', 'country', 'user']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = CustomUser.objects.create_user(**user_data)
        company_profile = CompanyProfile.objects.create(user=user, **validated_data)
        return company_profile

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user = instance.user

        serializer = CustomUserSerializer(user, data=user_data, partial=True)
        if serializer.is_valid():
            serializer.save()
        instance = super().update(instance, validated_data)
        return instance
