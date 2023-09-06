from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError, ValidationError
from .models import Consent

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    consent_given = serializers.BooleanField(write_only=True)  # Nouveau champ de consentement

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'consent_given']

    def create(self, validated_data):
        consent_given = validated_data.pop('consent_given', False)  # Retirer le consentement des données validées
        validated_data['password'] = make_password(validated_data.get('password'))
        user = User.objects.create(**validated_data)

        # Enregistrement du consentement de l'utilisateur si donné
        if consent_given:
            Consent.objects.create(user=user)
        
        return user

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email address already exists.")
        
        try:
            from validate_email_address import validate_email
            if not validate_email(value):
                raise serializers.ValidationError("Please provide a valid email address.")
        except ValidationError:
            raise serializers.ValidationError("Please provide a valid email address.")
        
        return value

    def validate_consent_given(self, value):
        if not value:
            raise serializers.ValidationError("Vous devez donner votre consentement pour vous inscrire.")
        return value
    
