from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.middleware.csrf import get_token
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post, Category
from .serializers import PostSerializer, CategorySerializer, CommentSerializer
from interactions.models import Like, Comment
from accounts.serializers import UserSerializer
from django.contrib.auth.models import User

@api_view(["GET"])
@permission_classes([AllowAny])
def csrf(request):
    return Response({"csrfToken": get_token(request)})

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    lookup_field = "slug"
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    def get_queryset(self):
        qs = Post.objects.select_related(
            "author", "author__profile", "category"
        ).annotate(
            like_count=Count("likes", distinct=True),
            comment_count=Count("comments", distinct=True)
        )

        user = self.request.user

        if self.action in ["update", "partial_update", "destroy"]:
            return qs.filter(author=user) if user.is_authenticated else qs.none()

        if self.action == "list":
            if user.is_authenticated and self.request.query_params.get("mine") == "1":
                qs = qs.filter(author=user)
            else:
                qs = qs.filter(status=Post.PUBLISHED)

            q = self.request.query_params.get("q", "").strip()
            category = self.request.query_params.get("category", "")
            sort = self.request.query_params.get("sort", "newest").lower()

            if q:
                qs = qs.filter(
                    Q(title__icontains=q) |
                    Q(excerpt__icontains=q) |
                    Q(content__icontains=q) |
                    Q(tags__icontains=q) |
                    Q(author__username__icontains=q)
                )

            if category:
                qs = qs.filter(category__slug=category)

            if sort == "oldest":
                qs = qs.order_by("published_at", "created_at")
            elif sort in ["popular", "most_liked", "most-liked"]:
                qs = qs.order_by("-like_count", "-published_at", "-created_at")
            else:
                qs = qs.order_by("-published_at", "-created_at")

            return qs

        if self.action == "retrieve":
            if user.is_authenticated:
                return qs.filter(Q(status=Post.PUBLISHED) | Q(author=user))
            return qs.filter(status=Post.PUBLISHED)
        if self.action in ["like", "comments"]:
            return qs.filter(status=Post.PUBLISHED)

        return qs
    def get_permissions(self):
        if self.action in ["create","update","partial_update","destroy","like"]:
            return [IsAuthenticated()]
        if self.action == "comments" and self.request.method == "POST":
            return [IsAuthenticated()]
        return [AllowAny()]
    def perform_create(self, serializer): serializer.save(author=self.request.user)
    def perform_update(self, serializer): serializer.save()
    @action(detail=True, methods=["post"])
    def like(self, request, slug=None):
        post = self.get_object()
        like, created = Like.objects.get_or_create(post=post,user=request.user)
        if not created:
            like.delete(); liked = False
        else: liked = True
        return Response({"liked":liked,"like_count":post.likes.count()})
    @action(detail=True, methods=["get","post"])
    def comments(self, request, slug=None):
        post = self.get_object()
        if request.method == "GET":
            qs = post.comments.select_related("user","user__profile").all()
            return Response(CommentSerializer(qs,many=True,context={"request":request}).data)
        serializer = CommentSerializer(data=request.data,context={"request":request})
        serializer.is_valid(raise_exception=True)
        serializer.save(post=post,user=request.user)
        return Response(serializer.data,status=201)

class CategoryListView(APIView):
    permission_classes = [AllowAny]
    def get(self,request): return Response(CategorySerializer(Category.objects.all(),many=True).data)

class DashboardView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        posts = Post.objects.filter(author=request.user).select_related("author","author__profile","category").annotate(like_count=Count("likes", distinct=True),comment_count=Count("comments", distinct=True),likes_total=Count("likes", distinct=True),comments_total=Count("comments", distinct=True))
        return Response({
            "total_posts":posts.count(),
            "published_posts":posts.filter(status=Post.PUBLISHED).count(),
            "draft_posts":posts.filter(status=Post.DRAFT).count(),
            "total_likes":sum(p.likes_total for p in posts),
            "total_comments":sum(p.comments_total for p in posts),
            "posts":PostSerializer(posts, many=True, context={"request":request}).data
        })

class ProfileView(APIView):
    permission_classes = [AllowAny]
    def get(self,request,username):
        user = get_object_or_404(User.objects.select_related("profile"),username=username)
        posts = Post.objects.filter(author=user,status=Post.PUBLISHED).select_related("category","author","author__profile").annotate(like_count=Count("likes"),comment_count=Count("comments"))
        return Response({"user":UserSerializer(user,context={"request":request}).data,"posts":PostSerializer(posts,many=True,context={"request":request}).data})

class CommentDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def patch(self,request,pk):
        comment = get_object_or_404(Comment,pk=pk,user=request.user)
        serializer = CommentSerializer(comment,data=request.data,partial=True,context={"request":request})
        serializer.is_valid(raise_exception=True); serializer.save()
        return Response(serializer.data)
    def delete(self,request,pk):
        comment = get_object_or_404(Comment,pk=pk,user=request.user)
        comment.delete(); return Response(status=204)
