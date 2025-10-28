from django.urls import path
from .views import login, logout, me, CustomTokenRefreshView

urlpatterns = [
    path('login', login, name='login'),
    path('login/', login, name='login-slash'),
    path('logout', logout, name='logout'),
    path('logout/', logout, name='logout-slash'),
    path('refresh', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('refresh/', CustomTokenRefreshView.as_view(), name='token_refresh-slash'),
    path('me', me, name='me'),
    path('me/', me, name='me-slash'),
]