from django.urls import include, path

from .views import FollowApiView, FollowListApiView

urlpatterns = [
    path('users/subscriptions/', FollowListApiView.as_view(),
         name='subscriptions'),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls')),
    path('users/<int:following_id>/subscribe/', FollowApiView.as_view()),
]
