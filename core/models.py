from django.db import models

# Create your models here.
class Theater(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

class Show(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    cover = models.ImageField(upload_to='show_covers/', blank=True, null=True)

    def __str__(self):
        return self.title

class Event(models.Model):
    title = models.CharField(max_length=255,blank=True,null=True)
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name='events', blank=True, null=True)
    theater = models.ForeignKey(
        Theater,
        on_delete=models.CASCADE,
        related_name='events'
    )
    event_date = models.DateTimeField()
    sales_start = models.DateTimeField()
    sales_end = models.DateTimeField()

    def __str__(self):
        return self.title or self.show.title

class Section(models.Model):
    theater = models.ForeignKey(Theater,on_delete=models.CASCADE,related_name="sections")
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Row(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="rows")
    row_number = models.CharField(max_length=5)
    seats_per_row = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.section} - Row {self.row_number}"


class SeatCategory(models.Model):
    theater = models.ForeignKey(
        Theater,
        on_delete=models.CASCADE,
        related_name="seat_categories"
    )
    color = models.CharField(
    max_length=7,
    default="#808080"
)
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    def __str__(self):
        return self.name
    

class EventSeatPrice(models.Model):

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="prices"
    )

    category = models.ForeignKey(
        SeatCategory,
        on_delete=models.CASCADE
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    class Meta:
        unique_together = (
            "event",
            "category"
        )

class Seat(models.Model):
    row = models.ForeignKey(Row, on_delete=models.CASCADE, related_name="seats")
    seat_number = models.CharField(max_length=10,blank=True,null=True)
    category = models.ForeignKey(SeatCategory, on_delete=models.PROTECT, related_name="seats", blank=True, null=True)
    
    def __str__(self):
        return f"Row {self.row.id} - Seat {self.seat_number}"

class Booking(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='bookings',
        null=True,
        blank=True
    )

    seat = models.ForeignKey(
        Seat,
        on_delete=models.CASCADE,
        related_name='bookings'
    )

    user_name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    image = models.ImageField(upload_to='booking_images/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['event', 'seat'],
                name='unique_event_seat'
            )
        ]

    def __str__(self):
        return self.user_name