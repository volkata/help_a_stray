from rest_framework import routers
from actions.views import ActionsListView, edit_action, contribute_treatment, ActionViewSet
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'actions', ActionViewSet, basename='action')  # <-- must be a ViewSet

urlpatterns = [
    path('', ActionsListView.as_view(), name='actions'),
    path('edit/<int:cat_id>/', edit_action, name='edit_action'),
    path('cat/<int:cat_id>/contribute/', contribute_treatment, name='contribute_treatment'),

    path('api/', include(router.urls)),
]