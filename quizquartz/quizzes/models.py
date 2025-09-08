from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import User
from uuid import uuid4


class Tag(models.Model):
    """Model representing a tag for quizzes."""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(
        verbose_name=_("Tag Name"),
        max_length=50,
        unique=True,
        help_text=_("Required. Enter the name of the tag. 50 characters or fewer."),
        error_messages={
            "unique": _("A tag with that name already exists."),
            "blank": _("This field cannot be blank."),
        },
    )
    is_private = models.BooleanField(
        default=False,
        verbose_name=_("Is Private"),
        help_text=_("Indicates whether the tag is private."),
    )

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    def __str__(self):
        return self.name


class QuizGroup(models.Model):
    """Model representing a group of quizzes."""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(
        verbose_name=_("Group Title"),
        max_length=100,
        unique=True,
        help_text=_(
            "Required. Enter the title of the quiz group. 100 characters or fewer."
        ),
        error_messages={
            "unique": _("A quiz group with that title already exists."),
            "blank": _("This field cannot be blank."),
        },
    )
    subtitle = models.CharField(
        verbose_name=_("Group Subtitle"),
        max_length=100,
        blank=True,
        help_text=_("Enter a subtitle for the quiz group. 100 characters or fewer."),
    )
    description = models.TextField(
        verbose_name=_("Group Description"),
        max_length=500,
        blank=True,
        help_text=_(
            "Enter a brief description of the quiz group. 500 characters or fewer."
        ),
    )
    created_by = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="quiz_groups",
        verbose_name=_("Created By"),
        help_text=_("User who created the quiz group."),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At"),
        help_text=_("Creation timestamp."),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated At"),
        help_text=_("Last update timestamp."),
    )

    class Meta:
        verbose_name = _("Quiz Group")
        verbose_name_plural = _("Quiz Groups")

    def __str__(self):
        return self.title


class Quiz(models.Model):
    """Model representing a quiz."""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    question = models.TextField(
        verbose_name=_("Question"),
        max_length=500,
        help_text=_("The question content in plain text. 500 characters or fewer."),
        error_messages={
            "blank": _("This field cannot be blank."),
        },
    )
    answer = models.JSONField(
        verbose_name=_("Answer"),
        help_text=_("The correct answer(s) for the quiz question."),
        error_messages={
            "blank": _("This field cannot be blank."),
        },
    )
    tags = models.ManyToManyField(
        to=Tag,
        blank=True,
        related_name="quizzes",
        verbose_name=_("Tags"),
        help_text=_("Tags associated with the quiz."),
    )
    related_group = models.ForeignKey(
        to=QuizGroup,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="quizzes",
        verbose_name=_("Quiz Group"),
        help_text=_("The group this quiz belongs to."),
    )
    is_checked = models.BooleanField(
        default=False,
        verbose_name=_("Is Checked"),
        help_text=_("Indicates whether the quiz has been checked."),
    )
    created_by = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="quizzes",
        verbose_name=_("Created By"),
        help_text=_("User who created the quiz."),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At"),
        help_text=_("Creation timestamp."),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated At"),
        help_text=_("Last update timestamp."),
    )

    class Meta:
        verbose_name = _("Quiz")
        verbose_name_plural = _("Quizzes")

    def __str__(self):
        return self.question
