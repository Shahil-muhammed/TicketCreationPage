from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('track/<int:pid>/', views.problem, name='problem'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('signin/', views.SignInView.as_view(), name='signin'),
    path('logout/', views.custom_logout, name='logout'),
]
