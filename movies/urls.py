from django.urls import path, include

from . import views

urlpatterns = [
    path("filter/", views.FilterMoviesView.as_view(), name = 'filter'),
    path("search/", views.Search.as_view(), name = 'search'),
    path("last/", views.MovieLast.as_view(), name = 'last'),
    path("most_popular/", views.MoviePopularView.as_view(), name = 'most_popular'),
    path('home/', views.HomeView.as_view(), name = 'home'),
    path('data-json', views.PictureView.as_view(), name = 'data-json'),
    path("add-views/", views.MostPopular.as_view(), name='add_views'),
    # path('hitcount/', include(('hitcount.urls', 'hitcount'), namespace='hitcount')),
    path("add-rating/", views.AddStarRating.as_view(), name='add_rating'),
    path("json-filter/", views.JsonFilterMoviesView.as_view(), name='json_filter'),
    path('', views.MoviesView.as_view(), name = 'movie_list'),
    path('<slug:slug>/', views.MovieDetailView.as_view(), name = 'movie_detail'),
    path('review/<int:pk>/', views.AddReview.as_view(), name = 'add_review'),
    path('actor/<str:slug>/', views.ActorView.as_view(), name = 'actor_detail'),
    
]