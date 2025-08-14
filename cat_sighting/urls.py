from django.urls import path, include
from rest_framework import routers
from cat_sighting import views
from cat_sighting.views import CatSightingViewSet

router = routers.DefaultRouter()
router.register(r'cat_sighting', CatSightingViewSet, basename='sighting')

urlpatterns = [
    # HTML views
    path('part1/', views.create_sighting_part1, name='part1'),
    path('new_cat/', views.create_sighting_new_cat, name='new_cat'),
    path('update_cat/<int:pk>/', views.create_sighting_existing_cat, name='update_cat'),

    # API endpoints
    path('api/', include(router.urls)),
]