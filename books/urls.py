
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import BookViewSet, AuthorViewSet, GenreViewSet, ConditionViewSet, BookRequestViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'authors', AuthorViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'conditions', ConditionViewSet)
router.register(r'book-requests', BookRequestViewSet)

urlpatterns = [
    path('', include(router.urls)),
]