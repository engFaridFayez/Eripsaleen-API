from rest_framework import serializers
from .models import Theater, Section, Row, Seat, Booking


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ['id', 'seat_number', 'is_booked']



class RowSerializer(serializers.ModelSerializer):
    seats = SeatSerializer(many=True, read_only=True, source='seat_set')

    class Meta:
        model = Row
        fields = ['id', 'row_number', 'seats_per_row', 'seats']


class SectionSerializer(serializers.ModelSerializer):
    rows = RowSerializer(many=True, read_only=True, source='row_set')

    class Meta:
        model = Section
        fields = ['id', 'name', 'rows']


class TheaterDetailSerializer(serializers.ModelSerializer):
    sections = SectionSerializer(many=True, read_only=True, source='section_set')

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
    class Meta:
        model = Section
        fields = ['id', 'theater', 'name']


# 📏 Row (simple CRUD)
class RowSerializerSimple(serializers.ModelSerializer):
    class Meta:
        model = Row
        fields = ['id', 'section', 'row_number', 'seats_per_row']


# 💺 Seat (simple CRUD)
class SeatSerializerSimple(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ['id', 'row', 'seat_number', 'is_booked']


# 🎟️ Booking
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'seat', 'user_name', 'created_at']
        read_only_fields = ['created_at']

    def validate(self, attrs):
        seat = attrs['seat']

        if seat.is_booked:
            raise serializers.ValidationError("This seat is already booked.")

        return attrs

    def create(self, validated_data):
        seat = validated_data['seat']
        seat.is_booked = True
        seat.save()

        return Booking.objects.create(**validated_data)