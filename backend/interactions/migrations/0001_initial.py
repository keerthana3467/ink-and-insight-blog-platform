from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.core.validators

class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL), ("blogs", "0001_initial")]
    operations = [
        migrations.CreateModel(name="Comment", fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("content", models.CharField(max_length=1000, validators=[django.core.validators.MinLengthValidator(2)])), ("created_at", models.DateTimeField(auto_now_add=True)), ("updated_at", models.DateTimeField(auto_now=True)), ("post", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="comments", to="blogs.post")), ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="comments", to=settings.AUTH_USER_MODEL))], options={"ordering": ["created_at"]}),
        migrations.CreateModel(name="Like", fields=[("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("created_at", models.DateTimeField(auto_now_add=True)), ("post", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="likes", to="blogs.post")), ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="likes", to=settings.AUTH_USER_MODEL))], options={"constraints": [models.UniqueConstraint(fields=("post", "user"), name="unique_user_post_like")]}),
    ]
