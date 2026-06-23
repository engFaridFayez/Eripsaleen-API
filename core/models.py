from django.db import models

# Create your models here.
class Theater(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

class Section(models.Model):
    theater = models.ForeignKey(Theater,on_delete=models.CASCADE,related_name="sections")
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Row(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="rows")
    row_number = models.PositiveIntegerField()
    seats_per_row = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.section} - Row {self.row_number}"

class Seat(models.Model):
    row = models.ForeignKey(Row, on_delete=models.CASCADE, related_name="seats")
    seat_number = models.CharField(max_length=10,blank=True,null=True)
    is_booked = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Row {self.row.id} - Seat {self.seat_number}"

class Booking(models.Model):
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, related_name="bookings")
    user_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_name