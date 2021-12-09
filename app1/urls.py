from django.urls import path,include

from app1 import views

urlpatterns = [
    path('', views.index ),
    path('registro', views.registro),
    path('login', views.login),
    path('logout', views.logout),
    path('friends', views.friends),
    path('logout', views.logout),
    path('user/<int:id>/', views.userProfile),
    path('user/<int:id>/add', views.addFriend),
    path('user/<int:id>/remove', views.remove),
]