from django.db import models


class Guestbook(models.Model):
    title = models.CharField(max_length=100)
    writer = models.CharField(max_length=30)
    content = models.TextField()
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} - {self.writer}'
