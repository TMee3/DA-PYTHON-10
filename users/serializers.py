from rest_framework import serializers
from django.utils import timezone
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'password', 'can_be_contacted', 'can_data_be_shared', 'birth_date')
        extra_kwargs = {
            'password': {'write_only': True, 'required': True}
        }

    def validate_birth_date(self, value):
        if value is None:
            raise serializers.ValidationError('La date de naissance est requise.')

        today = timezone.now().date()
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        if age < 15:
            raise serializers.ValidationError('L\'utilisateur doit avoir au moins 15 ans.')
        return value

    def validate_username(self, value):
        if get_user_model().objects.filter(username=value).exists():
            raise serializers.ValidationError("Ce nom d'utilisateur existe déjà.")
        return value

    def validate_email(self, value):
        if get_user_model().objects.filter(email=value).exists():
            raise serializers.ValidationError("Cette adresse e-mail est déjà utilisée.")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError('Le mot de passe doit contenir au moins 8 caractères.')
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = get_user_model().objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user
