from district import views
from django.urls import path

from district.views import CatsInDistrictListView

urlpatterns = [
    path('', views.home, name='home'),
    path('district/<int:pk>/', CatsInDistrictListView.as_view(), name='cats_in_district'),
    ]