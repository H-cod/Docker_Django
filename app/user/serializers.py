from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for User model"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', "name")
        extra_kwargs = {
            "password": {"write_only": True, "min_length": 5}
        }

    def create(self, validated_data):
        """ Create a new  user with encrypted password and return it"""
        email = validated_data.get('email')
        password = validated_data.get('password')
        name = validated_data.get('name')
        new_user = get_user_model().objects.create_user(email=email,
                                                        password=password,
                                                        name=name)
        return new_user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for User authentication object """

    email = serializers.CharField()
    password = serializers.CharField(style={
        "input_type": "password",
    }, trim_whitespace=False)

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(ruquest=self.context.get('request'),
                            username=email, password=password)
        if not user:
            msg = "Unable to authenticate with provided credentials"
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user

        return attrs
