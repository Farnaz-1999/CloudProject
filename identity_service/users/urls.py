from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView
)
from .views import SignUpUser

urlpatterns = [
    path('signup/', SignUpUser.as_view(), name='signup_user'),
    path('jwt/', include([
        path('', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    ])),
]
