from rest_framework import serializers

from bearer_auth.models import Token

class DeserializeUserDecryptedData(serializers.Serializer):

    jti = serializers.UUIDField()
    refresh = serializers.BooleanField()

class TokenData(serializers.ModelSerializer):

    class Meta:
        model = Token
        fields = ("active", "created_at", "expired", "expired_refresh")