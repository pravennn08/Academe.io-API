from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import IntegrityError, transaction
from rest_framework import serializers

User = get_user_model()

CREATABLE_ROLES = [
    "Teacher",
    "Student",
    "Parent",
]


class UserRegistrationSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(
        choices=CREATABLE_ROLES,
        write_only=True,
    )
    password = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
        style={"input_type": "password"},
    )
    password_confirm = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
        style={"input_type": "password"},
    )

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "password_confirm",
            "role",
        ]

    def validate_email(self, value: str) -> str:
        email = value.strip().lower()

        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError(
                "An account with this email already exists."
            )

        return email

    def validate(self, attrs):
        password = attrs["password"]
        password_confirm = attrs["password_confirm"]

        if password != password_confirm:
            raise serializers.ValidationError(
                {"password_confirm": "Passwords do not match."}
            )

        candidate_user = User(email=attrs["email"])

        try:
            validate_password(password, user=candidate_user)
        except DjangoValidationError as error:
            raise serializers.ValidationError(
                {"password": list(error.messages)}
            ) from error

        return attrs

    def create(self, validated_data):
        role = validated_data.pop("role")
        password = validated_data.pop("password")
        validated_data.pop("password_confirm")

        try:
            with transaction.atomic():
                user = User.objects.create_user(
                    password=password,
                    **validated_data,
                )

                group = Group.objects.get(name=role)
                user.groups.add(group)

                return user
        except IntegrityError as error:
            raise serializers.ValidationError(
                {"email": "An account with this email already exists."}
            ) from error


class UserSerializer(serializers.ModelSerializer):
    roles = serializers.SlugRelatedField(
        source="groups",
        slug_field="name",
        many=True,
        read_only=True,
    )

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "roles",
            "is_active",
        ]


class UserRegistrationResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    message = serializers.CharField()
    data = UserSerializer()
