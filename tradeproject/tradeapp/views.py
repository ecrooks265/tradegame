from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from .models import Profile, Round, Leaderboard
from .forms import *
from .tools import update_all_stock_sentiments

def home(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')
    else:
        return render(request, 'login.html')

def signup(request):
    if request.method == 'POST':
        user_form = UserSignupForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            Profile.objects.create(user=user)
            return redirect('home')
    else:
        user_form = UserSignupForm()

    return render(request, 'signup.html', {'user_form': user_form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    """Handle user logout."""
    logout(request)
    return redirect('home')

@login_required
def dashboard(request):
    """Render the user's dashboard with their trading stats and current round info."""
    profile = Profile.objects.get(user=request.user)
    rounds = Round.objects.filter(player1=profile) | Round.objects.filter(player2=profile)
    return render(request, 'dashboard.html', {'profile': profile, 'rounds': rounds})

@login_required
def trade(request):
    """Render the trading page where users can make trades."""
    return render(request, 'trade.html')

@login_required
def leaderboard(request):
    """Render the leaderboard page."""
    leaderboards = Leaderboard.objects.all().order_by('-total_points')
    return render(request, 'leaderboard.html', {'leaderboards': leaderboards})

@login_required
def profile(request):
    """Render the user profile page."""
    profile = Profile.objects.get(user=request.user)
    return render(request, 'profile.html', {'profile': profile})

@login_required
def create_game(request):
    if request.method == 'POST':
        form = GameCreationForm(request.POST)
        if form.is_valid():
            game = form.save(commit=False)
            game.created_by = request.user  # Associate the game with the current user
            game.save()
            return redirect('home')  # Redirect to a success page or game list
    else:
        form = GameCreationForm()

    return render(request, 'create-game.html', {'form': form})

def market_view(request):
    """View to manually trigger market updates (for testing purposes)."""
    update_all_stock_sentiments()
    stocks = Stock.objects.all()
    return render(request, 'market/market_update.html', {'stocks': stocks})

def market_update(request):
    """Updates the market state and returns the updated stock data."""
    stocks = Stock.objects.values('name', 'price')
    return JsonResponse(list(stocks), safe=False)
