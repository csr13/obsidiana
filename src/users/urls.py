from django.urls import path

from users import views


app_name = "users"

urlpatterns = [
    path(
        "refresh-token", 
        views.DecoratedTokenRefreshView.as_view(),
        name="refresh-token"
    ),
    path(
        "get-token",
        views.DecoratedTokenObtainPairView.as_view(),
        name="authenticate"
    )
]
