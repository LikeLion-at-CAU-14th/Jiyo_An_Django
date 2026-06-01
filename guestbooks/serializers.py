from rest_framework import serializers
from .models import Guestbook


class GuestbookSerializer(serializers.ModelSerializer):
    guestbook_id = serializers.IntegerField(source='id', read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Guestbook
        fields = [
            'guestbook_id',
            'title',
            'writer',
            'content',
            'password',
            'created_at',
        ]
        read_only_fields = [
            'guestbook_id',
            'created_at',
        ]