from django.urls import path
from control.views import SecondAdmin  
from .views import AssignerLoginView, AssignerLogoutView, AssignerSignupView,Lsolved,AssignerSolvedTickets as ast
from . import views
app_name = 'assigner'

urlpatterns = [
    path('', SecondAdmin, name="vendor"),  
    path('login/', AssignerLoginView.as_view(), name="assigner-login"),  
    path('logout/', AssignerLogoutView.as_view(), name="assigner-logout"),  
    path('signup/', AssignerSignupView.as_view(), name='assigner-signup'),  
    path('lsolved/',ast.as_view(),name='lsolved'),
    path('view_problems/<int:ticket_id>/',views.ProblemDetailView.as_view(),name="viewprob"),
]
