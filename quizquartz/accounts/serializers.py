from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
import re


User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""

    username = serializers.CharField(
        max_length=150,
        help_text="このフィールドは必須です。150文字以内。英字、数字、@/./+/-/_ のみ使用可能です。",
    )
    email = serializers.EmailField(
        max_length=254,
        help_text="このフィールドは必須です。254文字以内。正しいメールアドレスを入力してください。",
    )
    password = serializers.CharField(
        style={"input_type": "password"},
        write_only=True,
        help_text="このフィールドは必須です。8文字以上で、少なくとも1つの大文字、1つの小文字、1つの数字、1つの特殊文字を含めてください。",
    )
    password2 = serializers.CharField(
        style={"input_type": "password"},
        write_only=True,
        help_text="確認のため、もう一度パスワードを入力してください。",
    )

    class Meta:
        model = User
        fields = ("username", "email", "password", "password2")
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        password2 = data.get("password2")

        # Username uniqueness check
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                detail=f"**{username}**このユーザー名は既に使用されています。"
            )
        # Username format check
        if not re.match(pattern=r"^[\w.@+-]+$", string=username):
            raise serializers.ValidationError(
                detail=f"**{username}**このユーザー名は無効です。"
            )
        # Email uniqueness check
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                detail=f"**{email}**このメールアドレスは既に使用されています。"
            )
        # Password match check
        if password != password2:
            raise serializers.ValidationError(detail="パスワードが一致しません。")
        # Password complexity check
        if len(password) < 8:
            raise serializers.ValidationError(
                detail="パスワードは8文字以上である必要があります。"
            )
        if not re.search(pattern=r"[A-Z]", string=password):
            raise serializers.ValidationError(
                detail="パスワードには少なくとも1つの大文字が含まれている必要があります。"
            )
        if not re.search(pattern=r"[a-z]", string=password):
            raise serializers.ValidationError(
                detail="パスワードには少なくとも1つの小文字が含まれている必要があります。"
            )
        if not re.search(pattern=r"[0-9]", string=password):
            raise serializers.ValidationError(
                detail="パスワードには少なくとも1つの数字が含まれている必要があります。"
            )
        if not re.search(pattern=r"[!@#$%^&*(),.?\":{}|<>]", string=password):
            raise serializers.ValidationError(
                detail="パスワードには少なくとも1つの特殊文字が含まれている必要があります。"
            )

        return data

    def create(self, validated_data):
        validated_data.pop("password2")
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    """Serializer for user login."""

    username = serializers.CharField(max_length=150)
    password = serializers.CharField(
        style={"input_type": "password"}, trim_whitespace=False
    )

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        if username and password:
            user = authenticate(
                request=self.context.get("request"),
                username=username,
                password=password,
            )
            if not user:
                raise serializers.ValidationError(
                    detail="ログインに失敗しました。ユーザー名またはパスワードが正しくありません。",
                    code="authorization",
                )
        else:
            raise serializers.ValidationError(
                detail="ユーザー名とパスワードの両方を入力してください。",
                code="authorization",
            )

        data["user"] = user
        return data


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user details."""

    date_joined = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = User
        fields = ("username", "email", "nickname", "date_joined")


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for editing user details."""

    username = serializers.CharField(max_length=150)
    email = serializers.EmailField(max_length=254)
    nickname = serializers.CharField(max_length=30)

    class Meta:
        model = User
        fields = ("username", "email", "nickname")

    def validate(self, data):
        user_id = self.instance.id if self.instance else None
        username = data.get("username")
        email = data.get("email")
        nickname = data.get("nickname")

        if username and email and nickname:
            # Username uniqueness check
            if User.objects.exclude(id=user_id).filter(username=username).exists():
                raise serializers.ValidationError(
                    detail=f"**{username}**このユーザー名は既に使用されています。"
                )
            # Username format check
            if not re.match(pattern=r"^[\w.@+-]+$", string=username):
                raise serializers.ValidationError(
                    detail=f"**{username}**このユーザー名は無効です。"
                )
            # Email uniqueness check
            if User.objects.exclude(id=user_id).filter(email=email).exists():
                raise serializers.ValidationError(
                    detail=f"**{email}**このメールアドレスは既に使用されています。"
                )
            # Nickname uniqueness check
            if User.objects.exclude(id=user_id).filter(nickname=nickname).exists():
                raise serializers.ValidationError(
                    detail=f"**{nickname}**このニックネームは既に使用されています。"
                )
        else:
            raise serializers.ValidationError(
                detail="全てのフィールドを入力してください。"
            )

        return data

    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        instance.nickname = validated_data.get("nickname", instance.nickname)
        instance.save()
        return instance


class PasswordChangeSerializer(serializers.Serializer):
    """Serializer for changing user password."""

    old_password = serializers.CharField(
        style={"input_type": "password"}, trim_whitespace=False
    )
    new_password = serializers.CharField(
        style={"input_type": "password"}, trim_whitespace=False
    )
    new_password2 = serializers.CharField(
        style={"input_type": "password"}, trim_whitespace=False
    )

    def validate(self, data):
        user = self.context["request"].user
        old_password = data.get("old_password")
        new_password = data.get("new_password")
        new_password2 = data.get("new_password2")

        # Old password check
        if not user.check_password(old_password):
            raise serializers.ValidationError(
                detail="現在のパスワードが正しくありません。"
            )
        # New password match check
        if new_password != new_password2:
            raise serializers.ValidationError(detail="新しいパスワードが一致しません。")
        # New password complexity check
        if len(new_password) < 8:
            raise serializers.ValidationError(
                detail="新しいパスワードは8文字以上である必要があります。"
            )
        if not re.search(pattern=r"[A-Z]", string=new_password):
            raise serializers.ValidationError(
                detail="新しいパスワードには少なくとも1つの大文字が含まれている必要があります。"
            )
        if not re.search(pattern=r"[a-z]", string=new_password):
            raise serializers.ValidationError(
                detail="新しいパスワードには少なくとも1つの小文字が含まれている必要があります。"
            )
        if not re.search(pattern=r"[0-9]", string=new_password):
            raise serializers.ValidationError(
                detail="新しいパスワードには少なくとも1つの数字が含まれている必要があります。"
            )
        if not re.search(pattern=r"[!@#$%^&*(),.?\":{}|<>]", string=new_password):
            raise serializers.ValidationError(
                detail="新しいパスワードには少なくとも1つの特殊文字が含まれている必要があります。"
            )

        return data

    def save(self, **kwargs):
        user = self.context["request"].user
        new_password = self.validated_data["new_password"]
        user.set_password(new_password)
        user.save()
        return user
