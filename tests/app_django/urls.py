from pyx.apps.app_django.app_django.urls import *
from pyx.apps.app_django.utils import tag_to_view

from tests import test_1, test_2, test_3


urlpatterns = [path('1/', tag_to_view(test_1.__pyx__))]
