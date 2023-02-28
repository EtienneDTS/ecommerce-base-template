from django.urls import path


app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
]