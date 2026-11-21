from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError

def validate_image_size(image):
    if image.size > 3 * 1024 * 1024:
        raise ValidationError("Image must be 3 MB or smaller.")

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True,
        validators=[FileExtensionValidator(["jpg","jpeg","png","webp"]), validate_image_size])
    bio = models.CharField(max_length=280, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"{self.user.username}'s profile"
