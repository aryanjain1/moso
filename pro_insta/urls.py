from django.urls import path
from .views import retrieve_data, index, sign_up, user_logout, user_login

urlpatterns = [

    path('retrieve/<int:follower_count>/<int:following_count>/<str:category>/',
         retrieve_data, name="retrievedata"),
    path('', index, name="index"),
    path('register/', sign_up, name='register'),
    path('login/', user_login),
    path('logout/', user_logout),
]
