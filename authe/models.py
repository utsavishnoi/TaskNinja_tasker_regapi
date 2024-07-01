from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth import get_user_model

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        (1, 'user'),
        (2, 'tasker'),
    ]

    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='user')
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    about = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    service = models.CharField(max_length=100, blank=True, null=True)
    EXPERIENCE_CHOICES = [
        ('Less than 1 year', 'Less than 1 year'),
        ('1-2 years', '1-2 years'),
        ('2-3 years', '2-3 years'),
        ('More than 3 years', 'More than 3 years'),
    ]

    experience = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    skill_proof_pdf = models.CharField(max_length=1024, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group, related_name='custom_user_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions')
    is_approved = models.BooleanField(default=False)
    def __str__(self):
        return self.username

class Address(models.Model):
    user = models.ForeignKey(get_user_model(), related_name='addresses', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)
    full_address = models.TextField()

    def __str__(self):
        return f"{self.name}, {self.city}, {self.state}, {self.pincode}"

    class Meta:
        unique_together = ('user', 'name')  # Ensures name is unique per user

class TaskerSkillProof(models.Model):
    tasker = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='skill_proofs')
    pdf = models.CharField(blank=True, max_length=1024)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Tasker Skill Proof for {self.tasker.username}"
