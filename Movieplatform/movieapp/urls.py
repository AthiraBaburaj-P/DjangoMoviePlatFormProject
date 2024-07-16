
from django.urls import path
from . import views

# urlpatterns = [
#     path('', views.home, name='home'),
#     path('register/', views.register, name='register'),
#     path('login/', views.user_login, name='login'),
#     path('profile/', views.profile, name='profile'),
#     path('add_movie/', views.add_movie, name='add_movie'),
#     path('movies/', views.movie_list, name='movie_list'),
#     path('movies/category/<int:category_id>/', views.movies_by_category, name='movies_by_category'),
#     path('movies/<int:pk>/', views.movie_detail, name='movie_detail'),
#     path('movies/<int:pk>/delete/', views.delete_movie, name='delete_movie'),
#     path('movies/<int:pk>/edit/', views.edit_movie, name='edit_movie'),
#     path('search/', views.search_movies, name='search_movies'),

# ]


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('add_movie/', views.add_movie, name='add_movie'),
    path('movie_list/', views.movie_list, name='movie_list'),
    path('movie_list/category/<int:category_id>/', views.movies_by_category, name='movies_by_category'),
    path('movie_list/all/', views.movies_by_category, {'category_id': 0}, name='movies_all'),
    path('movie/<int:pk>/', views.movie_detail, name='movie_detail'),
    path('movie/edit/<int:pk>/', views.edit_movie, name='edit_movie'),
    path('movie/delete/<int:pk>/', views.delete_movie, name='delete_movie'),
    path('search/', views.search_movies, name='search_movies'),
]
