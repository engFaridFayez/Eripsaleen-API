from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Theater, Section, Row, Seat, Booking
from .serializers import (
    TheaterSerializer,
    TheaterDetailSerializer,
    SectionSerializerSimple,
    RowSerializerSimple,
    SeatSerializerSimple,
    BookingSerializer
)


# =============================================
#             For CRUD operarions
# =============================================
class TheaterViewSet(viewsets.ModelViewSet):
    queryset = Theater.objects.all()
    serializer_class = TheaterSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TheaterDetailSerializer
        return TheaterSerializer
    
class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializerSimple

class RowViewSet(viewsets.ModelViewSet):
    queryset = Row.objects.all()
    serializer_class = RowSerializerSimple

class SeatViewSet(viewsets.ModelViewSet):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializerSimple

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


# =============================================
#             For Front-end
# =============================================

class TheaterViewSet(viewsets.ModelViewSet):
    queryset = Theater.objects.all()
    serializer_class = TheaterSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TheaterDetailSerializer
        return TheaterSerializer

    @action(detail=True, methods=['get'])
    def seat_map(self, request, pk=None):
        theater = self.get_object()
        serializer = TheaterDetailSerializer(theater)
        return Response(serializer.data)