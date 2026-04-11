from django.urls import path
from django.views.generic import TemplateView

from .views import signup, token


urlpatterns = [
    path(
        'signup/',
        view=signup,
        name='signup'
    ),
    path(
        'token/',
        view=token,
        name='token'
    ),
]
