from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.core.validators
from accounts.models import validate_image_size

class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [migrations.CreateModel(name="Profile", fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("avatar", models.ImageField(blank=True, null=True, upload_to="avatars/", validators=[django.core.validators.FileExtensionValidator(["jpg", "jpeg", "png", "webp"]), validate_image_size])), ("bio", models.CharField(blank=True, max_length=280)), ("created_at", models.DateTimeField(auto_now_add=True)), ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="profile", to=settings.AUTH_USER_MODEL))]) ]
