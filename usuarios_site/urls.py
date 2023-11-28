from django.urls import path, include
from .views import UserRegisterView, UserLoginView, UserEditView

urlpatterns = [
    path('register/', UserRegisterView.as_view(),name="register"),
    path('login/', UserLoginView.as_view(), name="login"),
    path('editando-perfil/', UserEditView.as_view(), name="editar_perfil"),
]

