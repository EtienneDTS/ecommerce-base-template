from django.urls import path

from .views import signup, Login, Logout, profile


app_name = 'accounts'

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('profile/', profile, name='profile'),
]