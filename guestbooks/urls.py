from django.urls import path
from .views import GuestbookListCreateView, GuestbookDetailView

urlpatterns = [
    path('guestbooks/', GuestbookListCreateView.as_view()),
    path('guestbooks/<int:guestbook_id>/', GuestbookDetailView.as_view()),
]