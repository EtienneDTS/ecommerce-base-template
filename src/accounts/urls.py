from django.urls import path
from django.conf.urls.static import static

from .views import signup, Login, Logout, profile, change_password, newsletter
from Ecommerce import settings


app_name = 'accounts'

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('profile/', profile, name='profile'),
    path('change_password/', change_password, name='change_password'),
    path('newsletter/', newsletter, name='newsletter')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)