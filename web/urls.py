from django.urls import path
from rest_framework.routers import DefaultRouter
from .apiVIews import UniversityViewSet, MentorViewSet, MentorInUniversityViewset, CommentsViewSet, \
     CommentsInMentorsViewset
from . import views

router = DefaultRouter()
router.register('apiUniversity', UniversityViewSet, basename='university Names')
# router.register('apiGig', GigViewSet, basename='Gig Detail')
router.register('apiMentor', MentorViewSet, basename='Mentors DEtail')
router.register('mentorInUniversity', MentorInUniversityViewset, basename='Mentors In University')
router.register('apicomments', CommentsViewSet, basename="Comment Detail")
router.register('commentsInMentor', CommentsInMentorsViewset, basename="Comments In Mentors")
# router.register('gigInMentor', GigInMentor, basename="Gig in Mentor")

# urlpatterns = [

    # path('registerUser/', CustomRegisterView.as_view(), name='register new user'),

#     path("", views.index, name="index"),
#     path("login", views.login_view, name="login"),
#     path("register", views.register, name="register"),
#     path("supportedunis", views.supportedunis, name="supportedunis"),
#     path("logout", views.logout_view, name="logout"),
#     path("becomeamentor", views.becomeamentor, name="becomeamentor"),
#     path("uni/<str:university>", views.universities, name="university"),
#     path("checkout", views.checkout, name="checkout"),
#     path("account/edit", views.accountedit, name="accountedit"),
#     path("account/<str:mentorname>", views.mentorprofile, name="mentorprofile"),
# ]

urlpatterns = router.urls
