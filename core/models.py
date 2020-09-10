from django.db import models
from django.core.validators import validate_comma_separated_integer_list
from django.contrib.auth import get_user_model
from django.urls import reverse


__all__ = ['Paste', 'ExpiryLog']


class Paste(models.Model):
    class Meta:
        ordering = ('pk', )
    title = models.CharField(max_length=100)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    expiry = models.DateTimeField(null=True, blank=True)
    hits = models.PositiveIntegerField(default=0)
    size = models.PositiveIntegerField(default=0, editable=False)
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    language = models.ForeignKey(
        'Language',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    def save(self, *args, **kwargs):
        """On save, update estimated size of the paste."""
        self.size = sum([
            len(self.title.encode('utf-8')),
            len(self.body.encode('utf-8')),
        ])
        return super().save(*args, **kwargs)

    def view(self):
        self.hits += 1
        self.save()
        return self

    def get_absolute_url(self):
        return reverse('show_paste', kwargs={'paste_id': self.pk})


class Language(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class ExpiryLog(models.Model):
    expired_ids = models.CharField(blank=True,
                                   max_length=int(pow(2, 20)),
                                   validators=[validate_comma_separated_integer_list])
    timestamp = models.DateTimeField(auto_now_add=True)
    count = models.PositiveIntegerField(default=0)
    reclaimed_space = models.PositiveIntegerField(default=0)
    completed = models.BooleanField(default=False)
