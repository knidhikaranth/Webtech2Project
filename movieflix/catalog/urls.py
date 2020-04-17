from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('news/',views.news, name = 'news'),
	path('<str:username>/<str:movie>/rate/', views.rate, name = 'rate'),
	path('movies/', views.moviesAll.as_view(), name='all'),
	path('register/', views.signup, name = 'signup'),
	path('login/', views.login, name = 'login'),
	path('<str:username>/', views.added_user, name = 'added_user'),
	path('<str:username>/movies/', views.moviesAll.as_view(), name='all'),
	path('<str:username>/history/', views.history, name = 'history'),
	path('<str:username>/<str:movie>/',views.usingle, name = 'usingle'),
	path('<str:username>/history/<str:movie>/',views.usingle, name = 'usingle'),
	path('<str:username>/<str:movie>/history/', views.modhistory, name = 'modhistory'),
]