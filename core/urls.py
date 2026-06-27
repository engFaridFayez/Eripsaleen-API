from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    EventViewSet,
    TheaterViewSet,
    SectionViewSet,
    RowViewSet,
    SeatViewSet,
    BookingViewSet,
    MultiBookingView
)

router = DefaultRouter()

router.register(r'theaters', TheaterViewSet, basename='theater')
router.register(r'events', EventViewSet, basename='event')
router.register(r'sections', SectionViewSet, basename='section')
router.register(r'rows', RowViewSet, basename='row')
router.register(r'seats', SeatViewSet, basename='seat')
router.register(r'bookings', BookingViewSet, basename='booking')

urlpatterns = [
    path('', include(router.urls)),
    path(
        'multi-booking/',
        MultiBookingView.as_view(),
        name='multi-booking'
    ),
]