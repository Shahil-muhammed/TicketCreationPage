from django.urls import path
from . import views
app_name = 'control'
urlpatterns = [
    path('',views.SecondAdmin,name="SecondAdmin"),
    path('solved',views.solved,name="solved"),
    path('assigned',views.assigned,name="assigned"),
    path('rejected',views.rejected,name="rejected"),
    path('view_problems/<int:ticket_id>/',views.ProblemDetailView.as_view(),name="problemview"),
    path('admin_search/<int:ticket_id>/',views.Asearch.as_view(),name='asearch'),
]
