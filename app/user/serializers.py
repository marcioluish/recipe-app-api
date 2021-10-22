from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 5,
                'style': {
                    'input_type': 'password'
                }
            }
        }

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""

        """
        The "pop()" function on the dictionary is used to retrieve the value
        of a key while simultaneously removing the key from the dictionary.
        The purpose of overriding the "update()" function is to prevent the
        password being passed in as plain text, and instead, set it using the
        "set_password()" function so it gets encrypted. So what we do, is we
        use "pop()" to "pop" it out of the dictionary into a variable called
        password, and then pass the rest of the dictionary (excluding the
        password) through into the original "update()" function. Then we set
        the password using "set_password()".
        """
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={
            'input_type': 'password',
            'trim_whitespace': False
        }
    )

    # Function that validates our serializer and our credentials
    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs
