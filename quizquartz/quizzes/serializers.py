from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Tag, QuizGroup, Quiz


User = get_user_model()


class TagSerializer(serializers.ModelSerializer):
    """Serializer for listing tags."""

    class Meta:
        model = Tag
        fields = ("id", "name")


class QuizGroupSerializer(serializers.ModelSerializer):
    """Serializer for listing quiz groups."""

    created_by = serializers.CharField(source="created_by.nickname", read_only=True)

    class Meta:
        model = QuizGroup
        fields = ("id", "title", "subtitle", "description", "created_by")


class QuizGroupCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating quiz groups."""

    title = serializers.CharField(max_length=100)
    subtitle = serializers.CharField(max_length=200, required=False, allow_blank=True)
    description = serializers.CharField(
        max_length=500, required=False, allow_blank=True
    )

    class Meta:
        model = QuizGroup
        fields = ("title", "subtitle", "description")

    def validate(self, data):
        title = data.get("title")
        if QuizGroup.objects.filter(title=title).exists():
            raise serializers.ValidationError(
                detail="このタイトル名は別ユーザーが使用しています。"
            )

    def create(self, validated_data):
        quiz_group = QuizGroup.objects.create(**validated_data)
        return quiz_group


class QuizGroupUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating quiz groups."""

    title = serializers.CharField(max_length=100)
    subtitle = serializers.CharField(max_length=200, required=False, allow_blank=True)
    description = serializers.CharField(
        max_length=500, required=False, allow_blank=True
    )

    class Meta:
        model = QuizGroup
        fields = ("title", "subtitle", "description")

    def validate(self, data):
        title = data.get("title")
        instance = self.instance
        if QuizGroup.objects.filter(title=title).exclude(id=instance.id).exists():
            raise serializers.ValidationError(
                detail="このタイトル名は別ユーザーが使用しています。"
            )
        return data

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.subtitle = validated_data.get("subtitle", instance.subtitle)
        instance.description = validated_data.get("description", instance.description)
        instance.save()
        return instance


class QuizSerializer(serializers.ModelSerializer):
    """Serializer for listing quizzes."""

    tags = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")
    related_group = serializers.CharField(source="related_group.title", read_only=True)
    created_by = serializers.CharField(source="created_by.nickname", read_only=True)

    class Meta:
        model = Quiz
        fields = (
            "id",
            "question",
            "answer",
            "is_checked",
            "tags",
            "related_group",
            "created_by",
        )


class QuizCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating quizzes."""

    question = serializers.CharField(max_length=500)
    answer = serializers.JSONField()
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        required=False,
    )
    related_group = serializers.PrimaryKeyRelatedField(
        queryset=QuizGroup.objects.all(), required=False
    )

    class Meta:
        model = Quiz
        fields = ("question", "answer", "tags", "related_group")

    def validate(self, data):
        tags = data.get("tags", [])

        for tag in tags:
            if tag.is_private:
                raise serializers.ValidationError(detail="非公開タグが含まれています。")

        return data

    def create(self, validated_data):
        tags = validated_data.pop("tags", [])
        quiz = Quiz.objects.create(**validated_data)

        for tag in tags:
            quiz.tags.add(tag)

        return quiz


class QuizUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating quizzes."""

    question = serializers.CharField(max_length=500)
    answer = serializers.JSONField()
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        required=False,
    )
    related_group = serializers.PrimaryKeyRelatedField(
        queryset=QuizGroup.objects.all(), required=False
    )

    class Meta:
        model = Quiz
        fields = ("question", "answer", "tags", "related_group")

    def validate(self, data):
        tags = data.get("tags", [])

        for tag in tags:
            if tag.is_private:
                raise serializers.ValidationError(detail="非公開タグが含まれています。")

        return data

    def update(self, instance, validated_data):
        instance.question = validated_data.get("question", instance.question)
        instance.answer = validated_data.get("answer", instance.answer)

        tags = validated_data.get("tags", None)
        if tags is not None:
            instance.tags.set(tags)

        related_group = validated_data.get("related_group", None)
        if related_group is not None:
            instance.related_group = related_group

        instance.save()
        return instance
