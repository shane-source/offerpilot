from django.urls import path
from .views import board, create_application, move_card, notes, attachments

urlpatterns = [
    path("board/", board),
    path("board/create/", create_application),
    path("board/move/", move_card),

    path("app/<int:app_id>/notes/", notes),
    path("app/<int:app_id>/attachments/", attachments),
]
