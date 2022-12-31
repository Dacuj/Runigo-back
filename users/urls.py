from django.urls import URLPattern
from .apiViews import UserDetailViewset, UserDetail, PermissionViewSet, GroupViewSet, CustomRegisterView
# GoogleLoginView

from django.urls import path
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register('usr', UserDetailViewset, basename='User Detail')
router.register('permission', PermissionViewSet, basename='Permission')
router.register('group', GroupViewSet, basename='Group')

urlpatterns = [
path('userDetail', UserDetail.as_view()),
path('registerUser/', CustomRegisterView.as_view(), name='register new user'),
# path('updateUser', loggedInUserUpdate.as_view(), name='update user'),
# path('createUser', UserCreateViewSet.as_view()),
]


urlpatterns += router.urls