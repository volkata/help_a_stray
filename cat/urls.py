
from django.urls import path, include
from rest_framework import routers
from cat import views
from cat.views import CatViewSet

router = routers.DefaultRouter()
router.register(r'cats', CatViewSet, basename='cat')  # DRF API

urlpatterns = [

    path('<int:pk>/', views.cat_detail, name='cat_detail'),

    path('api/', include(router.urls)),
]