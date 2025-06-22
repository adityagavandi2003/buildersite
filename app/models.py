from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

# Create your models here.

USER_CATEGORIES = (
    ("builder", "Builder"),
    ("agent", "Agent"),
)
class AbstractUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(choices=USER_CATEGORIES,max_length=50)
    phone_number = models.CharField(
        max_length=16,
        validators=[
            RegexValidator(
                regex=r'^\+91 \d{10}$',
                message="Phone number must be entered in the format: '+91 9898999898'."
            )
        ],
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"<{self.category} name={self.user.username}>"

class Cutomer(models.Model):
    PROPERTY_TYPES = [
        ("residential", "Residential"),
        ("commercial", "Commercial"),
        ("plot", "Plot"),
        ("1bhk", "1 BHK"),
        ("2bhk", "2 BHK"),
        ("3bhk", "3 BHK"),
        ("4bhk", "4 BHK"),
        ("villa", "Villa"),
        ("studio", "Studio Apartment"),
        ("penthouse", "Penthouse"),
        ("duplex", "Duplex"),
        ("land", "Land"),
        ("office", "Office Space"),
        ("shop", "Shop/Showroom"),
        ("warehouse", "Warehouse"),
        ("farmhouse", "Farmhouse"),
    ]

    STATUS = (
        ('cancel','Cancel'),
        ('pending','Pending'),
        ('fulfilled','Fulfilled')
    )
    agent = models.ForeignKey(AbstractUser, verbose_name=("added by"), on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone_number = models.CharField(
        max_length=16,
        validators=[
            RegexValidator(
                regex=r'^\+91 \d{10}$',
                message="Phone number must be entered in the format: '+91 9898999898'."
            )
        ]
    )
    location = models.CharField(max_length=100)
    budget = models.DecimalField(max_digits=12, decimal_places=2)
    property_type = models.CharField(choices=PROPERTY_TYPES, max_length=50)
    status = models.CharField(choices=STATUS, max_length=50,blank=True,null=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"<Added by {self.agent.user.username} name={self.name}>"
    

