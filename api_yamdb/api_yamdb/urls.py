from django.contrib import admin
<<<<<<< HEAD
from django.urls import include, path
=======
from django.urls import path, include
>>>>>>> f9b892d (отзывы и комменты с заглушками)
from django.views.generic import TemplateView


urlpatterns = [
    path(
        'admin/',
        admin.site.urls
    ),
    # path(
    #     'api/v1/',
    #     include('api.urls')
    # ),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
    path('api/v1/', include('reviews.urls')),
]
