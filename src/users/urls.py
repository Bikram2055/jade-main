from django.urls import path
from rest_framework.routers import SimpleRouter

from src.users import views
from src.users.views import UserViewSet

users_router = SimpleRouter()

users_router.register(r'users', UserViewSet)

urlpatterns = [
    path("address/", views.AddressView.as_view()),
]
