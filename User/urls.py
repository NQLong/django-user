from Api.views import create_user
from django.urls import path, include, re_path
from User.views import create_user, get_user, list_user, update_user, delete_user, update_profile

profile_pattern = [
    path("/update", update_profile)
]

urlpatterns = [
    path('/list', list_user),
    path('/create', create_user),
    path('/update', update_user),
    path('/remove', delete_user),
    path('', get_user),
    re_path(r'/(?P<user_id>[0-9a-f-]+)/profile',include(profile_pattern))

    # path('/profile', include(profile_pattern))
]
