import re
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError

def validate_cover_size(image):
    if image.size > 5 * 1024 * 1024: raise ValidationError("Cover image must be 5 MB or smaller.")

class Category(models.Model):
    name = models.CharField(max_length=70, unique=True)
    slug = models.SlugField(max_length=90, unique=True)
    description = models.CharField(max_length=220, blank=True)
    def __str__(self): return self.name

class Post(models.Model):
    DRAFT = "draft"; PUBLISHED = "published"
    STATUS_CHOICES = [(DRAFT,"Draft"),(PUBLISHED,"Published")]
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=180)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    content = models.TextField()
    excerpt = models.CharField(max_length=280, blank=True)
    cover = models.ImageField(upload_to="covers/", blank=True, null=True,
        validators=[FileExtensionValidator(["jpg","jpeg","png","webp"]), validate_cover_size])
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="posts")
    tags = models.CharField(max_length=240, blank=True, help_text="Comma-separated tags")
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=DRAFT)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    class Meta: ordering = ["-published_at","-created_at"]
    def save(self, *args, **kwargs):
        from django.utils import timezone
        if not self.slug:
            base = slugify(self.title)[:180] or "story"; candidate = base; i = 2
            while Post.objects.filter(slug=candidate).exclude(pk=self.pk).exists():
                candidate = f"{base}-{i}"; i += 1
            self.slug = candidate
        if self.status == self.PUBLISHED and not self.published_at: self.published_at = timezone.now()
        if self.status == self.DRAFT: self.published_at = None
        if not self.excerpt and self.content:
            self.excerpt = re.sub("<[^>]+>", " ", self.content).strip()[:260]
        super().save(*args, **kwargs)
    @property
    def reading_minutes(self):
        words = len(re.sub("<[^>]+>", " ", self.content).split())
        return max(1, (words + 199)//200)
    def __str__(self): return self.title
