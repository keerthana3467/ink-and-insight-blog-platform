from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from .models import Category, Post
from interactions.models import Like

class BlogApiTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="writer",password="strong-pass-123")
        self.category = Category.objects.create(name="Tech",slug="tech")
        self.post = Post.objects.create(author=self.user,title="A sample story",content="<p>This is enough useful content for a test.</p>",category=self.category,status="published")
        self.client = APIClient()
    def test_public_feed_hides_drafts(self):
        Post.objects.create(author=self.user,title="Private draft",content="<p>Draft body content here.</p>")
        response = self.client.get("/api/posts/")
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(response.data),1)
    def test_like_requires_auth_and_is_unique(self):
        self.client.force_authenticate(self.user)
        first = self.client.post(f"/api/posts/{self.post.slug}/like/")
        second = self.client.post(f"/api/posts/{self.post.slug}/like/")
        self.assertTrue(first.data["liked"])
        self.assertFalse(second.data["liked"])
        self.assertEqual(Like.objects.filter(post=self.post,user=self.user).count(),0)
    def test_only_author_can_update(self):
        other = User.objects.create_user(username="other",password="strong-pass-123")
        self.client.force_authenticate(other)
        response = self.client.patch(f"/api/posts/{self.post.slug}/",{"title":"Hacked"})
        self.assertEqual(response.status_code,404)
