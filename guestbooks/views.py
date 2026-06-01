from django.shortcuts import render
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Guestbook
from .serializers import GuestbookSerializer


class GuestbookListCreateView(APIView):
    def get(self, request):
        guestbooks = Guestbook.objects.all().order_by('-created_at')
        serializer = GuestbookSerializer(guestbooks, many=True)

        return Response(
            {
                'guestbooks': serializer.data
            },
            status=status.HTTP_200_OK
        )

    def post(self, request):
        serializer = GuestbookSerializer(data=request.data)

        if serializer.is_valid():
            guestbook = serializer.save(
                password=make_password(serializer.validated_data['password'])
            )

            return Response(
                {
                    'message': '방명록이 작성되었습니다.',
                    'guestbook_id': guestbook.id
                },
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GuestbookDetailView(APIView):
    def delete(self, request, guestbook_id):
        guestbook = get_object_or_404(Guestbook, id=guestbook_id)

        password = request.data.get('password')

        if not password:
            return Response(
                {
                    'error': '비밀번호를 입력해주세요.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if not check_password(password, guestbook.password):
            return Response(
                {
                    'error': '비밀번호가 일치하지 않습니다.'
                },
                status=status.HTTP_403_FORBIDDEN
            )

        guestbook.delete()

        return Response(
            {
                'message': '방명록이 삭제되었습니다.'
            },
            status=status.HTTP_200_OK
        )