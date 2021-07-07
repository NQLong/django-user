
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # path('auth/', include('Auth.urls')),
    path('user', include('User.urls'))
]
