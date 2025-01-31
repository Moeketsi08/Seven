from django.db import models
class Province(models.Model):
    PROVINCE_CHOICES = [
        ('EC', 'Eastern Cape'),
        ('GP', 'Gauteng'),
        ('KZN', 'KwaZulu-Natal'),
        ('LP', 'Limpopo'),
        ('MP', 'Mpumalanga'),
        ('NC', 'Northern Cape'),
        ('NW', 'North West'),
        ('WC', 'Western Cape'),
        ('FS', 'Free State')
    ]
    province = models.CharField(choices=PROVINCE_CHOICES, max_length=50, null=True, unique=True)
    created = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.province

class Address(models.Model):
    unit_number = models.CharField(max_length=20, blank=True, null=True)  # Optional field
    building_name = models.CharField(max_length=100, blank=True, null=True)  # Optional field
    street_number = models.CharField(max_length=20, blank=True, null=True)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.street}, {self.postal_code}, {self.city}, {self.province}" 
