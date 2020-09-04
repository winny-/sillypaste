from django.db import models
from django.core.validators import validate_comma_separated_integer_list


__all__ = ['Paste', 'ExpiryLog']


class Paste(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField(unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    expiry = models.DateTimeField(null=True, blank=True)
    hits = models.PositiveIntegerField(default=0)
    size = models.PositiveIntegerField(default=0)

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


class ExpiryLog(models.Model):
    expired_ids = models.CharField(blank=True,
                                   max_length=int(pow(2, 20)),
                                   validators=[validate_comma_separated_integer_list])
    timestamp = models.DateTimeField(auto_now_add=True)
    count = models.PositiveIntegerField(default=0)
    reclaimed_space = models.PositiveIntegerField(default=0)
    completed = models.BooleanField(default=False)
