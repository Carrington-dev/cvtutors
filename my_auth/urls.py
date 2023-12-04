from django.urls import path, include
from . import views as my_auth_views
from rest_framework import routers
from django.contrib.auth import views as auth_views

router = routers.DefaultRouter()

urlpatterns = [
    path("", my_auth_views.home, name='home'),
    path("about/", my_auth_views.about, name='about'),
    path('our-tutors/', my_auth_views.ProfileListView.as_view(), name='tutors'),
    path('courses/', my_auth_views.CourseListView.as_view(), name='courses'),
    
    path('course/<int:year>/<int:month>/<int:day>/<slug:slug>/<int:pk>/', my_auth_views.course, name='course'),
    path('course-mk/overview/<int:pk>/', my_auth_views.courseEnrol, name='course-mk'),

    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path("product/<int:id>/", my_auth_views.product, name='home'),
    path('sign-in/', my_auth_views.login_view, name="login"),
    path('sign-out/', my_auth_views.logout_view, name="logout"),
    path('logout-success/', my_auth_views.logout_success, name="logout-success"),
    path('register/', my_auth_views.signup, name="register"),
    path('tutor-apply/', my_auth_views.tutor_register, name="tutor_register"),
    path('profile/', my_auth_views.profile, name="profile"),
    path('tprofile/', my_auth_views.tprofile, name="tprofile"),
    path('update-profile/', my_auth_views.profile_pic, name="profile_pic"),
    path('form-success/', my_auth_views.form_submitted, name="form_submitted"),
    path('verify_email_sent/', my_auth_views.verify_email_sent, name="verify_email_sent"),

    # EX
    # path('forgot-password/', my_auth_views.registration_view, name='forgot'),

    
    # Password reset links (ref: https://github.com/django/django/blob/master/django/contrib/auth/views.py)
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), 
        name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'), 
        name='password_change'),

    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'),
     name='password_reset_done'),

    
    path('user-verify-existance/<uidb64>/<token>/', my_auth_views.account_verification, name='account_verification'),

    path('password-reset-confirm/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), 
    name='password_reset_confirm'),
    path('password_reset/', my_auth_views.password_reset_request, name='password_reset'),
    # path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'), name='password_reset'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
      name='password_reset_complete'),
]