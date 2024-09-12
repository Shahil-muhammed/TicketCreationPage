from django.urls import path
from . import views
app_name = 'control'
urlpatterns = [
    path('',views.SecondAdmin,name="SecondAdmin"),
    path('solved',views.solved,name="solved"),
]
