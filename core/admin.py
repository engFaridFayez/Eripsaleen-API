from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Theater, Section, Row, Seat, Booking


@admin.register(Theater)
class TheaterAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'location']
    search_fields = ['name']

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'theater']
    list_filter = ['theater']
    search_fields = ['name']

@admin.register(Row)
class RowAdmin(admin.ModelAdmin):
    list_display = ['id', 'section', 'row_number', 'seats_per_row']
    list_filter = ['section']

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ['id', 'row', 'seat_number', 'is_booked']
    list_filter = ['is_booked', 'row']
    search_fields = ['seat_number']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'seat', 'user_name', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user_name']