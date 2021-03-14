from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views import defaults as default_views
from django.views.generic import TemplateView

from .views import (combination_list,
                    member_edit, member_list, member_new,
                    meet_test)

app_name = 'coffee'

urlpatterns = [
    path('combination_list', combination_list, name='combination_list'),
    # path('make_permutations', make_permutations, name='make_permutations'),
    path('meet_test', meet_test, name='meet_test'),
    re_path('member/(?P<pk>\d+)', member_edit, name='member_edit'),
    path('member_list', member_list, name='member_list'),
    path('member_new', member_new, name='member_new'),
]