from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView

from .views import make_permutations
app_name = 'coffee'

urlpatterns = [
    path('make_permutations', make_permutations, name='make_permutations'),
]