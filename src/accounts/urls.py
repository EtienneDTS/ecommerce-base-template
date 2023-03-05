from django.urls import path

from .views import signup, Login, Logout, profile, change_password


app_name = 'accounts'

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('profile/', profile, name='profile'),
    path('change_password/', change_password, name='change_password'),
]