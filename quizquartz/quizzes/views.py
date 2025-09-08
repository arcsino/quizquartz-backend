from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from .models import Tag, QuizGroup, Quiz
from .serializers import (
    TagSerializer,
    QuizGroupSerializer,
    QuizGroupCreateSerializer,
    QuizGroupUpdateSerializer,
    QuizSerializer,
    QuizCreateSerializer,
    QuizUpdateSerializer,
)
import re


class TagListAPIView(generics.ListAPIView):
    """Tag list view."""

    queryset = Tag.objects.filter(is_private=False).order_by("name")
    serializer_class = TagSerializer


class QuizGroupListAPIView(generics.ListAPIView):
    """Quiz group list view."""

    queryset = QuizGroup.objects.all().order_by("-created_at")
    serializer_class = QuizGroupSerializer


class QuizGroupDetailAPIView(generics.RetrieveAPIView):
    """Quiz group detail view."""

    queryset = QuizGroup.objects.all()
    serializer_class = QuizGroupSerializer


class QuizListAPIView(generics.ListAPIView):
    """Quiz list view."""

    queryset = Quiz.objects.all().order_by("-created_at")
    serializer_class = QuizSerializer


class QuizDetailAPIView(generics.RetrieveAPIView):
    """Quiz detail view."""

    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer


class QuizGroupCreateAPIView(generics.CreateAPIView):
    """Quiz group create view."""

    serializer_class = QuizGroupCreateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            quiz_group = serializer.save(created_by=request.user)
            return Response(
                data={
                    "message": "クイズグループの作成に成功しました。",
                    "quiz_group": QuizGroupSerializer(quiz_group).data,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuizGroupUpdateAPIView(generics.UpdateAPIView):
    """Quiz group update view."""

    queryset = QuizGroup.objects.all()
    serializer_class = QuizGroupUpdateSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, pk, *args, **kwargs):
        quiz_group = get_object_or_404(queryset=QuizGroup, pk=pk)

        if quiz_group.created_by != request.user:
            return Response(
                data={"error": "権限がありません。"},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = self.get_serializer(quiz_group, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                data={
                    "message": "クイズグループの更新に成功しました。",
                    "quiz_group": QuizGroupSerializer(quiz_group).data,
                },
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuizGroupDeleteAPIView(generics.DestroyAPIView):
    """Quiz group delete view."""

    queryset = QuizGroup.objects.all()
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk, *args, **kwargs):
        quiz_group = get_object_or_404(queryset=QuizGroup, pk=pk)

        if quiz_group.created_by != request.user:
            return Response(
                data={"error": "権限がありません。"},
                status=status.HTTP_403_FORBIDDEN,
            )

        quiz_group.delete()
        return Response(
            data={"message": "クイズグループの削除に成功しました。"},
            status=status.HTTP_200_OK,
        )


class QuizCreateAPIView(generics.CreateAPIView):
    """Quiz create view."""

    serializer_class = QuizCreateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        tags = request.data.get("tags", [])
        related_group = request.data.get("related_group", None)

        if tags:
            for tag_id in tags:
                # UUID validation
                if not re.match(
                    pattern=r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
                    string=tag_id,
                ):
                    return Response(
                        data={"error": "無効なタグID形式です。"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                # Tag existence check
                if not Tag.objects.filter(id=tag_id).exists():
                    return Response(
                        data={"error": "存在しないタグが含まれています。"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
        if related_group:
            related_group = get_object_or_404(QuizGroup, id=related_group)
            if related_group.created_by != request.user:
                return Response(
                    data={
                        "error": "このクイズグループにクイズを追加する権限がありません。"
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            quiz = serializer.save(created_by=request.user)
            return Response(
                data={
                    "message": "クイズの作成に成功しました。",
                    "quiz": QuizSerializer(quiz).data,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuizUpdateAPIView(generics.UpdateAPIView):
    """Quiz update view."""

    queryset = Quiz.objects.all()
    serializer_class = QuizUpdateSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, pk, *args, **kwargs):
        quiz = get_object_or_404(queryset=Quiz, pk=pk)
        tags = request.data.get("tags", [])
        related_group = request.data.get("related_group", None)

        if quiz.created_by != request.user:
            return Response(
                data={"error": "権限がありません。"},
                status=status.HTTP_403_FORBIDDEN,
            )
        if tags:
            for tag_id in tags:
                # UUID validation
                if not re.match(
                    pattern=r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
                    string=tag_id,
                ):
                    return Response(
                        data={"error": "無効なタグID形式です。"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                # Tag existence check
                if not Tag.objects.filter(id=tag_id).exists():
                    return Response(
                        data={"error": "存在しないタグが含まれています。"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
        if related_group:
            related_group = get_object_or_404(QuizGroup, id=related_group)
            if related_group.created_by != request.user:
                return Response(
                    data={
                        "error": "このクイズグループにクイズを追加する権限がありません。"
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

        serializer = self.get_serializer(quiz, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                data={
                    "message": "クイズの更新に成功しました。",
                    "quiz": QuizSerializer(quiz).data,
                },
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuizDeleteAPIView(generics.DestroyAPIView):
    """Quiz delete view."""

    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk, *args, **kwargs):
        quiz = get_object_or_404(queryset=Quiz, pk=pk)

        if quiz.created_by != request.user:
            return Response(
                data={"error": "権限がありません。"},
                status=status.HTTP_403_FORBIDDEN,
            )

        quiz.delete()
        return Response(
            data={"message": "クイズの削除に成功しました。"},
            status=status.HTTP_200_OK,
        )
