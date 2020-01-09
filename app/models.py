from django.db import models


class RegExp(models.Model):
    pattern = models.CharField(max_length=255)

    def __str__(self):
        return self.pattern


class Message(models.Model):
    with_file = models.BooleanField(default=False)
    pattern_found = models.BooleanField(default=False)
    pattern = models.CharField(max_length=255, blank=True)
    text = models.TextField(blank=True)
    filetype = models.CharField(max_length=40, blank=True)
    file_name = models.CharField(max_length=100, blank=True)
    file_link = models.CharField(max_length=255, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Message {}'.format(self.id)

