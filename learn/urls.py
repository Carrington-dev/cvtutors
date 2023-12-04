from django.urls import path
from . import views

urlpatterns = [
    path('content-order/', views.ContentOrderView.as_view(), name='content_order'),
    path("course-new/", views.CourseCreateView.as_view(), name="new_course"),
    path("course-update/<int:pk>/", views.CourseUpdateView.as_view(), name="update_course"),
    path("course-module/new/<int:pk>/", views.module_create, name="new_module"),
    path("courses-favorite/", views.my_likes, name="likes"),
    path("courses-enrolled/", views.my_courses, name="my_courses"),
    path("course-update/<int:pk>/", views.ModuleUpdateView.as_view(), name="update_module"),
    path('course-like/<int:pk>/', views.LikeCourseView, name="like_course"),
    path('course-complete/<int:pk>/', views.complete_course, name="complete_course"),
    path('course-module-complete/<int:pk>/', views.CompleteModule, name="complete_module"),
    path('course-modules-complete/', views.module_done, name="module_done"),
    path('course-certificate-<int:pk>/', views.generate_certificate, name='certificate'),
    path('search/', views.SearchResultsListView.as_view(), name='search_results'), # new



]