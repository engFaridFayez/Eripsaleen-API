from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.views import APIView
from .serializers import MultiBookingSerializer
from rest_framework.response import Response
from .models import Show, Theater, Section, Row, Seat, Booking,Event
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import (
    TheaterSerializer,
    TheaterDetailSerializer,
    SectionSerializerSimple,
    RowSerializerSimple,
    SeatSerializerSimple,
    BookingSerializer,
    EventSerializer,
    EventSectionSerializer,
    ShowSerializer,
    ShowDetailSerializer
)

class ShowViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Show.objects.prefetch_related(
        "events"
    )

    def get_serializer_class(self):

        if self.action == "retrieve":
            return ShowDetailSerializer

        return ShowSerializer
# =============================================
#             For CRUD operarions
# =============================================
class TheaterViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Theater.objects.all()
    serializer_class = TheaterSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TheaterDetailSerializer
        return TheaterSerializer
    

class EventViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    @action(detail=True, methods=['get'])
    def seat_map(self, request, pk=None):

        event = self.get_object()

        sections = Section.objects.filter(
            theater=event.theater
        ).prefetch_related(
            'rows__seats'
        )

        serializer = EventSectionSerializer(
            sections,
            many=True,
            context={'event': event}
        )

        return Response({
            'event_id': event.id,
            'event_title': event.title,
            'theater': event.theater.name,
            'sections': serializer.data
        })

class SectionViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Section.objects.all()
    serializer_class = SectionSerializerSimple

class RowViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Row.objects.all()
    serializer_class = RowSerializerSimple

class SeatViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Seat.objects.all()
    serializer_class = SeatSerializerSimple

class BookingViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


# =============================================
#             For Front-end
# =============================================

class TheaterViewSet(viewsets.ModelViewSet):
    queryset = Theater.objects.all()
    serializer_class = TheaterSerializer
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TheaterDetailSerializer
        return TheaterSerializer

    @action(detail=True, methods=['get'])
    def seat_map(self, request, pk=None):
        theater = self.get_object()
        serializer = TheaterDetailSerializer(theater)
        return Response(serializer.data)
    


import json

class MultiBookingView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):

        data = request.data.dict()   # ← دي المهمة

        data["event"] = int(data["event"])

        data["attendees"] = json.loads(request.data["attendees"])
        data["seats"] = json.loads(request.data["seats"])

        if "email" in request.data:
            data["email"] = request.data["email"]

        if "phone_number" in request.data:
            data["phone_number"] = request.data["phone_number"]

        if "image" in request.FILES:
            data["image"] = request.FILES["image"]

        serializer = MultiBookingSerializer(data=data)

        serializer.is_valid(raise_exception=True)

        bookings = serializer.save()

        return Response(
            {
                "message": f"{len(bookings)} seats booked successfully"
            },
            status=status.HTTP_201_CREATED
        )