from django.urls import path, include
import .views import UserRegisterView

urlpatterns = [
    path('register/', UserRegisterView.as_view(),name="register"),

]
