from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<component_name>[\w-]+)', views.one, name='pattern_library_component'),
    url(r'^', views.all, name='pattern_library'),
    url(r'^examples', views.index),
]
