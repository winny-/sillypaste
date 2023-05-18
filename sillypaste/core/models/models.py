from django.db import models
from django.db.models import Q
from django.db.models.functions import Lower
from django.core.validators import validate_comma_separated_integer_list
from django.contrib.auth import get_user_model
from django.urls import reverse
from collections import namedtuple


__all__ = ['Paste', 'Language', 'ExpiryLog']


class PasteManager(models.Manager):
    def filter_fulltext(self, text):
        if not text:
            return self.all()
        return self.filter(
            Q(body__icontains=text)
            | Q(title__icontains=text)
            | Q(author__username__icontains=text)
        )


class PublicPasteManager(PasteManager):
    def get_queryset(self):
        return super().get_queryset().filter(private=False)


class Paste(models.Model):
    class Meta:
        ordering = ('pk',)

    title = models.CharField(max_length=100)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    expiry = models.DateTimeField(null=True, blank=True)
    freeze_hits = models.BooleanField(default=False, blank=True)
    private = models.BooleanField(default=False, blank=True)
    hits = models.PositiveIntegerField(default=0)
    size = models.PositiveIntegerField(default=0, editable=False)
    author = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, blank=True, null=True
    )
    language = models.ForeignKey(
        'Language', on_delete=models.SET_NULL, blank=True, null=True
    )

    objects = PasteManager()
    public_objects = PublicPasteManager()

    def save(self, *args, **kwargs):
        """On save, update estimated size of the paste."""
        self.size = sum(
            [len(self.title.encode('utf-8')), len(self.body.encode('utf-8'))]
        )
        return super().save(*args, **kwargs)

    def view(self):
        if not self.freeze_hits:
            self.hits += 1
            self.save()
        return self

    def get_absolute_url(self):
        return reverse('show_paste', kwargs={'paste_id': self.pk})

    BODY_SQUARE_DIMENSIONS = namedtuple('dimensions', ['columns', 'rows'])(
        30, 9
    )  # cols, rows

    def body_square(self):
        lines = self.body.split('\n')[: self.BODY_SQUARE_DIMENSIONS.rows]
        return '\n'.join(
            line[: self.BODY_SQUARE_DIMENSIONS.columns] for line in lines
        )

    @property
    def renderable(self):
        return (
            self.language
            and self.language.name in Language.RENDERABLE_LANGUAGES
        )


class Language(models.Model):

    # Used to always ensure they are valid.
    RENDERABLE_LANGUAGES = frozenset({'markdown', 'org-mode'})

    class Meta:
        ordering = (Lower('name'),)

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class ExpiryLog(models.Model):

    MAX_ENTRIES = 200

    expired_ids = models.CharField(
        blank=True,
        max_length=int(pow(2, 20)),
        validators=[validate_comma_separated_integer_list],
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    user_cutoff = models.DateTimeField(auto_now_add=True)
    paste_count = models.PositiveIntegerField(default=0)
    reclaimed_space = models.PositiveIntegerField(default=0)
    user_count = models.PositiveIntegerField(default=0)
    completed = models.BooleanField(default=False)
