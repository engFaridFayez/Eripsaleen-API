from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    TheaterViewSet,
    SectionViewSet,
    RowViewSet,
    SeatViewSet,
    BookingViewSet
)

router = DefaultRouter()

router.register(r'theaters', TheaterViewSet, basename='theater')
router.register(r'sections', SectionViewSet, basename='section')
router.register(r'rows', RowViewSet, basename='row')
router.register(r'seats', SeatViewSet, basename='seat')
router.register(r'bookings', BookingViewSet, basename='booking')

urlpatterns = [
    path('', include(router.urls)),
]