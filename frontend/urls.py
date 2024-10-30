from django.urls import path
from . import views

urlpatterns = [
   path('', views.index, name='index'),
   path('addTestPart', views.add_test_part, name='addTestPart'),
]