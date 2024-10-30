from django.urls import path, include
from . import views

urlpatterns = [
   path('run', views.run_code.as_view()),
   path('addTestCase', views.add_test_case.as_view()),
   path('deleteTestCase', views.delete_test_case.as_view()),
   path('updateTestCase', views.update_test_case.as_view()),
   path('getTestCase', views.get_test_case.as_view()),
]