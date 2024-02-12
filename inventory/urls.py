from django.urls import path
from .views import RegisterView, LoginView, ItemsView, ItemView, CategoryView, LogoutView, ForgotPasswordView, VerifyView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('forgotpassword/', ForgotPasswordView.as_view(), name='forgotpassword'),
    path('items/', ItemsView.as_view(), name='items'),
    path('item/', ItemView.as_view(), name='item'),
    path('category/', CategoryView.as_view(), name='category'),
    path('verify/', VerifyView.as_view(), name='verify'),
]