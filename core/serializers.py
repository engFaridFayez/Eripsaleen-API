from rest_framework import serializers
from .models import SeatCategory, Show, Theater, Section, Row, Seat, Booking,Event
from django.db import transaction

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ['id', 'seat_number']

class RowSerializer(serializers.ModelSerializer):
    seats = SeatSerializer(many=True, read_only=True)

    class Meta:
        model = Row
        fields = ['id', 'row_number', 'seats_per_row', 'seats']


class SectionSerializer(serializers.ModelSerializer):
    rows = RowSerializer(many=True, read_only=True)

    class Meta:
        model = Section
        fields = ['id', 'name', 'rows']

class EventSerializer(serializers.ModelSerializer):
    theater_name = serializers.CharField(source="theater.name", read_only=True)
    show_name = serializers.CharField(source="show.title", read_only=True)

    class Meta:
        model = Event
        fields = [
            'id',
            'title',
            'theater',
            'theater_name',
            'event_date',
            'sales_start',
            'sales_end',
            'show',
            'show_name'
        ]

class TheaterDetailSerializer(serializers.ModelSerializer):
    sections = SectionSerializer(many=True, read_only=True)

    class Meta:
        model = Theater
        fields = ['id', 'name', 'location', 'sections']


# Simple Theater (list/create)
class TheaterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theater
        fields = ['id', 'name', 'location']


# Section (simple CRUD)
class SectionSerializerSimple(serializers.ModelSerializer):
    theater_name = serializers.CharField(
        source="theater.name",
        read_only=True
    )

    class Meta:
        model = Section
        fields = [
            "id",
            "theater",
            "theater_name",
            "name"
        ]


# 📏 Row (simple CRUD)
class RowSerializerSimple(serializers.ModelSerializer):
    section_name = serializers.CharField(
    source="section.name",
    read_only=True
    )
    theater_name = serializers.CharField(
        source="section.theater.name",
        read_only=True
    )
    class Meta:
        model = Row
        fields = ['id',"theater_name", 'section','section_name', 'row_number', 'seats_per_row']


# 💺 Seat (simple CRUD)
class SeatSerializerSimple(serializers.ModelSerializer):
    row_name = serializers.CharField(
        source="row.row_number",
        read_only=True
    )

    section_name = serializers.CharField(
        source="row.section.name",
        read_only=True
    )

    theater_name = serializers.CharField(
        source="row.section.theater.name",
        read_only=True
    )

    category = serializers.SerializerMethodField()

    def get_category(self, obj):
        if obj.category:
            return {
                "id": obj.category.id,
                "name": obj.category.name,
                "color": obj.category.color,
            }
        return None

    class Meta:
        model = Seat
        fields = [
            "id",
            "row",
            "row_name",
            "section_name",
            "seat_number",
            "theater_name",
            "category",
        ]

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            'id',
            'event',
            'seat',
            'user_name',
            'created_at'
        ]
        read_only_fields = ['created_at']


class EventSeatSerializer(serializers.ModelSerializer):
    is_booked = serializers.SerializerMethodField()
    section = serializers.SerializerMethodField()
    row_number = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    class Meta:
        model = Seat
        fields = [
            "id",
            "seat_number",
            "is_booked",
            "section",
            "row_number",
            "category",
            "price",
        ]


    def get_category(self, obj):
        if not obj.category:
            return None

        return {
            "id": obj.category.id,
            "name": obj.category.name,
            "color": obj.category.color,
        }
        


    def get_price(self, obj):
        if not obj.category or obj.category.price is None:
            return 0

        return obj.category.price
    
    def get_is_booked(self, obj):
        event = self.context.get('event')

        return Booking.objects.filter(
            event=event,
            seat=obj
        ).exists()

    def get_section(self, obj):
        return obj.row.section.name

    def get_row_number(self, obj):
        return obj.row.row_number


class EventRowSerializer(serializers.ModelSerializer):
    seats = serializers.SerializerMethodField()


    class Meta:
        model = Row
        fields = ['id', 'row_number', 'seats', 'section']

    def get_seats(self, obj):
        event = self.context.get('event')

        return EventSeatSerializer(
            obj.seats.all(),
            many=True,
            context={'event': event}
        ).data



class EventSectionSerializer(serializers.ModelSerializer):
    rows = EventRowSerializer(
    many=True,
    read_only=True
    )


    class Meta:
        model = Section
        fields = ['id', 'name', 'rows']

class MultiBookingSerializer(serializers.Serializer):
    event = serializers.IntegerField()
    attendees = serializers.ListField(child=serializers.CharField(max_length=255),min_length=1)
    email = serializers.EmailField(required=False, allow_blank=True)
    phone_number = serializers.CharField(max_length=20, required=False, allow_blank=True)
    image = serializers.ImageField(required=False,allow_null=True)
    seats = serializers.ListField(
        child=serializers.IntegerField(),
        min_length=1
    )

    def create(self, validated_data):
        event_id = validated_data["event"]
        seat_ids = validated_data["seats"]
        attendees = validated_data["attendees"]
        email = validated_data.get("email")
        phone_number = validated_data.get("phone_number")
        image = validated_data.get("image")

        with transaction.atomic():

            event = Event.objects.get(id=event_id)

            seats = Seat.objects.select_for_update().filter(
                id__in=seat_ids
            )

            if seats.count() != len(seat_ids):
                raise serializers.ValidationError(
                    "One or more seats do not exist."
                )

            already_booked = Booking.objects.filter(
                event=event,
                seat__in=seats
            )

            if already_booked.exists():
                raise serializers.ValidationError(
                    "One or more seats are already booked."
                )

            bookings = []

            for seat, attendee in zip(seats, attendees):
                bookings.append(
                    Booking(
                        event=event,
                        seat=seat,
                        user_name=attendee,
                        phone_number=phone_number,
                        email=email,
                        image=image
                    )
                )

            Booking.objects.bulk_create(bookings)

        return bookings
    



class ShowEventSerializer(serializers.ModelSerializer):
    theater = serializers.StringRelatedField()

    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "theater",
            "event_date"
        ]

class ShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Show
        fields = [
            "id",
            "title",
            "description",
            "cover"
        ]

class ShowDetailSerializer(serializers.ModelSerializer):

    events = ShowEventSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Show
        fields = [
            "id",
            "title",
            "description",
            "cover",
            "events"
        ]




class SectionDropdownSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ["id", "name"]

class RowDropdownSerializer(serializers.ModelSerializer):
    class Meta:
        model = Row
        fields = ["id", "row_number"]

class RowDropdownSerializer(serializers.ModelSerializer):
    class Meta:
        model = Row
        fields = ["id", "row_number"]




class GenerateSeatsSerializer(serializers.Serializer):
    prefix = serializers.CharField(max_length=10)
    start = serializers.IntegerField(min_value=1)
    end = serializers.IntegerField(min_value=1)
    category = serializers.PrimaryKeyRelatedField(
        queryset=SeatCategory.objects.all()
    )
    def validate(self, data):
        if data["start"] > data["end"]:
            raise serializers.ValidationError(
                "Start number must be less than or equal to End number."
            )

        return data
    





class SeatCategorySerializer(serializers.ModelSerializer):
    seats_count = serializers.SerializerMethodField()

    class Meta:
        model = SeatCategory
        fields = [
            "id",
            "theater",
            "name",
            "color",
            "seats_count",
            "price"
        ]

    def get_seats_count(self, obj):
        return obj.seats.count()

    def validate(self, attrs):
        theater = attrs.get(
            "theater",
            getattr(self.instance, "theater", None)
        )

        name = attrs.get(
            "name",
            getattr(self.instance, "name", None)
        )

        queryset = SeatCategory.objects.filter(
            theater=theater,
            name__iexact=name
        )

        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError({
                "name": "This category already exists for this theater."
            })

        return attrs