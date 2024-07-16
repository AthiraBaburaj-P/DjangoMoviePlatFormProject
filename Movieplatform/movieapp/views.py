
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, ProfileForm, MovieForm, ReviewForm
from .models import Movie, Review, Category, Profile

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            Profile.objects.create(user=user, first_name=user_form.cleaned_data['first_name'], last_name=user_form.cleaned_data['last_name'])
            login(request, user)
            return redirect('login')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'register.html', {'user_form': user_form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('movie_list')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('login')
    else:
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profile.html', {'profile_form': profile_form})

@login_required
def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.added_by = request.user
            movie.save()
            return redirect('movie_list')
    else:
        form = MovieForm()
    return render(request, 'add_movie.html', {'form': form})


def movie_list(request):
    movies = Movie.objects.all()
    categories = Category.objects.all()
    return render(request, 'movie_list.html', {'movies': movies, 'categories': categories})

def search_movies(request):
    query = request.GET.get('q', '')
    movies = Movie.objects.filter(title__icontains=query) if query else Movie.objects.none()
    categories = Category.objects.all()
    return render(request, 'movie_list.html', {'movies': movies, 'categories': categories, 'search_query': query})



# def movies_by_category(request, category_id):
#     category = get_object_or_404(Category, pk=category_id)
#     movies = Movie.objects.filter(category=category)
#     categories = Category.objects.all()
#     return render(request, 'movie_list.html', {'movies': movies, 'categories': categories, 'selected_category': category})


def movies_by_category(request, category_id):
    if category_id == 0:
        movies = Movie.objects.all()
        selected_category = None
    else:
        category = get_object_or_404(Category, pk=category_id)
        movies = Movie.objects.filter(category=category)
        selected_category = category
    categories = Category.objects.all()
    return render(request, 'movie_list.html', {'movies': movies, 'categories': categories, 'selected_category': selected_category})


@login_required
def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.movie = movie
            review.save()
            return redirect('movie_detail', pk=movie.pk)
    else:
        review_form = ReviewForm()
    reviews = movie.reviews.all()
    return render(request, 'movie_detail.html', {'movie': movie, 'reviews': reviews, 'review_form': review_form})

@login_required
def delete_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.user == movie.added_by:
        movie.delete()
        return redirect('movie_list')
    else:
        return redirect('movie_detail', pk=pk)

@login_required
def edit_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.user != movie.added_by:
        return redirect('movie_detail', pk=pk)

    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('movie_detail', pk=movie.pk)
    else:
        form = MovieForm(instance=movie)
    return render(request, 'edit_movie.html', {'form': form, 'movie': movie})


