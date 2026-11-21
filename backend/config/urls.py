from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from blogs.views import PostViewSet, CategoryListView, DashboardView, ProfileView, CommentDetailView, csrf
from accounts.views import register, login_view, logout_view, me

router = DefaultRouter()
router.register("posts", PostViewSet, basename="post")
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/csrf/", csrf),
    path("api/auth/register/", register),
    path("api/auth/login/", login_view),
    path("api/auth/logout/", logout_view),
    path("api/auth/me/", me),
    path("api/categories/", CategoryListView.as_view()),
    path("api/dashboard/", DashboardView.as_view()),
    path("api/profiles/<str:username>/", ProfileView.as_view()),
    path("api/comments/<int:pk>/", CommentDetailView.as_view()),
    path("api/", include(router.urls)),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
