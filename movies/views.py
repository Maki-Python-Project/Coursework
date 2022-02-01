from datetime import timedelta
from operator import mod
from re import template
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from django.db.models import Count
from django.views.generic import ListView, DetailView
from django.views.generic.base import TemplateView, View
from django.db.models import Sum
from django.utils import timezone

from .models import  Movie, Category, Actor, Genre, Picture, Rating, Reviews, UpdateViews
from .forms import  ReviewForm, RatingForm, PopularForm




from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# from .models import StudentApplying
from django.contrib.auth.models import User
from django.db.models import F

from movies import models




class GenreYear:
    """Жанры и года выхода фильмов"""

    def get_genres(self):
        return Genre.objects.all()
    
    def get_titles(self):
        return Movie.objects.order_by("-title").values("title").distinct()

    def get_years(self):
        return Movie.objects.order_by("-year").values("year").distinct()[:]

    def get_categories(self):
        return Category.objects.all()


import random
class MoviesView(GenreYear, ListView):
    """Список фильмов"""
    model = Movie
    queryset = Movie.objects.order_by('?')
    paginate_by = 9


class MovieLast(GenreYear, ListView):
    model = Movie
    queryset = Movie.objects.order_by("-year")[:6]
    paginate_by = 6

class MoviePopularView(GenreYear, ListView):
    model = Movie
    queryset = Movie.objects.order_by("-views")[:6]
    paginate_by = 6

# class MoviePopular(GenreYear, ListView):
#     model = Movie
#     queryset = Movie.objects.order_by("-views")
#     # template_name = 'movies/most_popular.html'
#     paginate_by = 4
#     def get_queryset(self):
#         queryset = Movie.objects.filter().update(views='views' + 1)
#         return queryset

    # Movie.objects.filter(pk=model.pk).update(views=('views') + 1)


class MovieDetailView(GenreYear, DetailView):
    """Полное описание фильма"""
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    slug_field = "url"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["star_form"] = RatingForm()
        
        
        return context


class AddReview(View):
    """Отзывы"""

    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.movie = movie
            form.save()
        return redirect(movie.get_absolute_url())


class ActorView(GenreYear, DetailView):
    """Вывод информации о актере"""
    model = Actor
    template_name = 'movies/actor.html'
    slug_field = "name"


class FilterMoviesView(GenreYear, ListView):
    """Фильтр фильмов"""
    paginate_by = 6

    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(genres__in=self.request.GET.getlist("genre"))|
            Q(category_id__in=self.request.GET.getlist("category")) 
        ).distinct()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["year"] = ''.join([f"year={x}&" for x in self.request.GET.getlist("year")])
        context["genre"] = ''.join([f"genre={x}&" for x in self.request.GET.getlist("genre")])
        context["category"] = ''.join([f"category={x}&" for x in self.request.GET.getlist("category")])
       
        return context


class JsonFilterMoviesView(ListView):
    """Фильтр фильмов в json"""

    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(genres__in=self.request.GET.getlist("genre"))
        ).distinct().values("title", "tagline", "url", "poster")
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = list(self.get_queryset())
        return JsonResponse({"movies": queryset}, safe=False)


class AddStarRating(View):
    """Добавление рейтинга фильму"""

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                movie_id=int(request.POST.get("movie")),
                defaults={'star_id': int(request.POST.get("star"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)

class Search(GenreYear, ListView):

    paginate_by = 2

    def get_queryset(self):
        return Movie.objects.filter(title__icontains = self.request.GET.get("q"))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f'q={self.request.GET.get("q")}&'
        return context

from django.db.models import Count, F
from django.http import HttpResponse, HttpResponseRedirect

class MostPopular(GenreYear, ListView):
    # def applyStatus(request):
    #     if "applybtn" in request.POST:
    #         profil = Movie.objects.all().update(
    #             views = F('views')+1
    #         )
            
    #         # profil.save(update_fields=["applied"])
    #         return redirect('movie_list')
    #     return HttpResponse('Not done')
    def post(self, request, pk=None):
        
        if "applybtn" in request.POST:
            profil = Movie.objects.filter(title=self.request.POST.get('applybtn')).update(
                views = F('views')+1
            )
            print(request.GET.get('applybtn'))
            res = 1
            return redirect('movie_list')
        return HttpResponse('Not done')

from django.core import serializers
from django.http import JsonResponse

class HomeView(TemplateView):
    template_name = 'movies/home.html'

class PictureView(View):
    def get(self, request):
        qs = Picture.objects.all()
        data = serializers.serialize('json', qs)
        return JsonResponse({'data': data}, safe=False)