
from django.urls import path
from drf_advanced_token import views

urlpatterns = [
    path('login/', views.GetToken.as_view(), name="adv_token_login"),
    path('token/', views.TokenAuth.as_view(), name="adv_token"),
    path('logout/', views.Logout.as_view(), name="adv_token_logout"),
]