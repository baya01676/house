from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class UserProfile(AbstractUser):
    user_name = models.CharField(max_length=30)
    phone_number = PhoneNumberField(null=True, blank=True)
    RoleChoices = (
        ('admin', 'admin'),
        ('seller', 'seller'),
        ('buyer', 'buyer'),)
    role = models.CharField(max_length=30, choices=RoleChoices)
    date_registered = models.DateTimeField(auto_now_add=True)


class City(models.Model):
    city_name = models.CharField(max_length=100, null=True, blank=True)
    city_image = models.ImageField(upload_to='city_image')

    def __str__(self):
        return self.city_name


class District(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='districts')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.city} - {self.name}"


class Property(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    PROPERTY_TYPE_CHOICES = (
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ('land', 'Land'),
        ('commercial', 'Commercial'),)
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPE_CHOICES)
    region = models.CharField(max_length=100)
    city = models.ManyToManyField(City, related_name='properties')  # Изменил related_name
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='properties')
    address = models.CharField(max_length=50)
    area = models.FloatField(help_text="Площадь в м²")
    price = models.DecimalField(max_digits=12, decimal_places=2)
    rooms = models.PositiveIntegerField()
    floor = models.PositiveIntegerField()
    total_floors = models.PositiveIntegerField()
    CONDITION_CHOICES = (
        ('new', 'new'),
        ('good', 'good'),
        ('needs_repair', 'needs_repair'),)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    seller = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='properties')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_avg_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return round(sum([i.rating for i in reviews]) / reviews.count(), 1)
        return 0

    def get_count_people(self):
        return self.reviews.count()

    def get_price_property(self):
        return self.price


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='property_image')
    image = models.ImageField(upload_to='properties/images/')

    def __str__(self):
        return f"Image for {self.property.id}"


class PropertyDocument(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='documents')
    document = models.FileField(upload_to='properties/documents/')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Review(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='authored_reviews')
    seller = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='received_reviews')
    rating = models.PositiveSmallIntegerField(choices=((i, i) for i in range(1, 6)))
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review {self.rating}/5 from {self.author} to {self.seller}"