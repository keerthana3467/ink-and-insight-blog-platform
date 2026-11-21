import bleach
from django.contrib.auth.models import User
from rest_framework import serializers
from accounts.serializers import UserSerializer
from .models import Post, Category
from interactions.models import Comment

ALLOWED_TAGS = ["p","br","strong","b","em","i","u","h2","h3","h4","ul","ol","li","blockquote","a","code","pre"]
ALLOWED_ATTRS = {"a":["href","title","target","rel"]}
class CategorySerializer(serializers.ModelSerializer):
    class Meta: model = Category; fields = ["id","name","slug","description"]

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(source="user", read_only=True)
    can_edit = serializers.SerializerMethodField()
    class Meta:
        model = Comment; fields = ["id","content","created_at","updated_at","author","can_edit"]
        read_only_fields = ["id","created_at","updated_at"]
    def get_can_edit(self,obj): return bool(self.context["request"].user.is_authenticated and obj.user_id == self.context["request"].user.id)

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)
    category_slug = serializers.CharField(source="category.slug", read_only=True)
    like_count = serializers.IntegerField(read_only=True)
    comment_count = serializers.IntegerField(read_only=True)
    liked = serializers.SerializerMethodField()
    reading_minutes = serializers.IntegerField(read_only=True)
    cover_url = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ["id","title","slug","content","excerpt","cover","cover_url","category","category_name","category_slug","tags","status","featured","created_at","updated_at","published_at","author","like_count","comment_count","liked","reading_minutes"]
        read_only_fields = ["id","slug","created_at","updated_at","published_at","author","like_count","comment_count","liked","reading_minutes","cover_url"]
    def get_liked(self,obj):
        user = self.context["request"].user
        return user.is_authenticated and obj.likes.filter(user=user).exists()
    def get_cover_url(self,obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.cover.url) if obj.cover and request else (obj.cover.url if obj.cover else None)
    def validate_content(self,value):
        cleaned = bleach.clean(value, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRS, protocols=["http","https","mailto"], strip=True)
        if len(bleach.clean(cleaned, tags=[], strip=True).strip()) < 10:
            raise serializers.ValidationError("Write at least 10 characters of blog content.")
        return cleaned
    def validate_title(self,value):
        if len(value.strip()) < 4: raise serializers.ValidationError("Title must be at least 4 characters.")
        return value.strip()
